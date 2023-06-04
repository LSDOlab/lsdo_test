import sys
import argparse
import shutil
import pathlib
import fnmatch
import json
import pytest


description = 'Python testing framework that builds on pytest and adds ' \
    + '(1) testing of run scripts (examples and tutorials) and ' \
    + '(2) tags for tests'

current_working_dir = pathlib.Path.cwd()
build_dir = pathlib.Path('.lt')


def _get_rel_paths_and_names(search_string):
    """
    Search current working directory for file names of interest.

    Parameters
    ----------
    search_string : str
        Pattern to search for in current working directory, e.g., '**/test_*.py'.

    Returns
    -------
    list of (rel_dir_path, file_name)
        Relative directory paths and file names.
    """
    rel_paths_and_names = list()

    for abs_file_path in current_working_dir.glob(search_string):
        rel_file_path = abs_file_path.relative_to(current_working_dir)
        file_name = rel_file_path.name
        rel_dir_path = rel_file_path.parent
        rel_paths_and_names.append((rel_dir_path, file_name))

    return rel_paths_and_names


def _read_file(rel_file_path):
    with open(rel_file_path, 'r') as f:
        # Read as list of lines with no newline characters
        return f.read().splitlines()
    

def _write_file(new_lines, rel_file_path):
    rel_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Add newline character at the end of each line
    new_lines = [line + '\n' for line in new_lines]

    with open(rel_file_path, 'w') as f:
        f.writelines(new_lines)


def _read_ipynb_file(rel_file_path):
    with open(rel_file_path, 'r') as f:
        ipynb_dict = json.load(f)

    lines = list()
    for cell in ipynb_dict['cells']:
        for line in cell['source']:
            # Don't add markdown lines
            if cell['cell_type'] == 'markdown':
                if not line[:5] == '##tu' and not line[:4] == '##ex':
                    break
            
            lines.append(line.replace('\n', ''))
        lines.append('')
    return lines


def _get_script_tags(line, directive, rel_file_path):
    """
    Search the given line of code for the directive.

    Parameters
    ----------
    line : str
        Line of code.
    directive : str
        Directive to search for, e.g., '##test'.

    Returns
    -------
    script_tags : list of str or None
        None if directive not found; or list of tags as strings.
    """
    directive_index = line.find(directive)
    # No directive found
    if directive_index == -1:
        return None, directive_index
    # Directive found
    else:
        script_tags = line[directive_index:].split(' ')
        # Directive is in the string, but it is not followed by an empty space or new line
        if script_tags[0] != directive:
            raise Exception('In file {}, {} is invalid'.format(rel_file_path, directive))
        # Return the script_tags
        else:
            return script_tags[1:], directive_index


def _is_match(script_tags, command_prompt_tags):
    """
    Return a boolean whether there is a match between any script tag and any command-line tag.
    """
    # Assume no match, unless '*' is in the command-line tags
    match = '*' in command_prompt_tags

    # Search for a match between any command-line tag and any tag in the current test
    for command_prompt_tag in command_prompt_tags:
        for script_tag in script_tags:
            if fnmatch.fnmatch(script_tag, command_prompt_tag):
                match = True
    return match


def _convert_to_test(old_lines):
    """
    Encapsulate this run script in one big test function.
    """
    new_lines = list()
    new_lines.append('def test():')
    for old_line in old_lines:
        new_lines.append(' ' * 4 + old_line)

    return new_lines


def lsdo_test_command():
    """
    The function that is called when 'lsdo_test' is run at a command prompt (Terminal)
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog='lsdo_test',
        description=description,
    )
    parser.add_argument(
        'tags', type=str, nargs='*', default='',
        help='Use "\*" to run all tests; ' 
            + 'or use one or more tags to run a specific subset of tests. '
            + 'Tests are run if there is *any* match between'
            + 'any tag here and any tag in the test.'
            + 'We use the fnmatch library to test for matches (see its docs for reference).'
            + 'The pattern "\*" matches any string; and "\?" matches any single character.',
    )
    parser.add_argument(
        '-k', '--keep', default=False, action='store_true', 
        help='Keep (do not delete) generated pytest files',
    )
    args = parser.parse_args()
    command_prompt_tags = args.tags

    # If the build directory exists, delete it
    if build_dir.is_dir():
        shutil.rmtree(build_dir)

    build_dir.mkdir()

    # Process test files
    for rel_dir_path, file_name in _get_rel_paths_and_names('**/test_*.py'):
        rel_file_path = rel_dir_path / file_name

        old_lines = _read_file(rel_file_path)

        new_lines = list()
        new_lines.append('import pytest')
        
        new_lines.append('')
        for old_line in old_lines:
            script_tags, directive_index = _get_script_tags(old_line, '##test', rel_file_path)

            # No directive in this line
            if script_tags is None:
                new_line = old_line
            # The directive was found in this line
            else:
                # There is a match---run the test
                if _is_match(script_tags, command_prompt_tags):
                    new_line = old_line
                # Skip the test
                else:
                    new_line = old_line[:directive_index] + '@pytest.mark.skip()'

            new_lines.append(new_line)

        _write_file(new_lines, build_dir / rel_file_path)

    # Process example/tutorial files
    for script_type in ['ex', 'tu']:
        for extension_type in ['py', 'ipynb']:
            for rel_dir_path, file_name in _get_rel_paths_and_names(
                '**/{}_*.{}'.format(script_type, extension_type)
            ):
                old_rel_file_path = rel_dir_path / file_name

                if extension_type is 'py':
                    old_lines = _read_file(old_rel_file_path)
                    new_rel_file_path = rel_dir_path / ('test_' + file_name)
                elif extension_type is 'ipynb':
                    old_lines = _read_ipynb_file(old_rel_file_path)
                    new_rel_file_path = rel_dir_path / ('test_' + file_name[:-5] + 'py')

                # Look for directive
                for old_line in old_lines:
                    script_tags, directive_index = _get_script_tags(old_line, '##test', old_rel_file_path)

                    # Directive found---break with this tags value
                    if script_tags:
                        break
                # No directive found---accept as no tag
                else:
                    script_tags = []

                # There is a match---encapsulate in test function, rename to a test file
                if _is_match(script_tags, command_prompt_tags):
                    new_lines = list()
                    new_lines.append('import warnings')
                    new_lines.append('warnings.filterwarnings("ignore")')
                    new_lines.append('import matplotlib.pyplot as plt')
                    new_lines.append('plt.ion()')
                    new_lines.extend(_convert_to_test(old_lines))

                    _write_file(new_lines, build_dir / new_rel_file_path)

    pytest.main([build_dir])

    if not args.keep:
        shutil.rmtree(build_dir)