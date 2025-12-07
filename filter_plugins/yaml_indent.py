"""Custom filter to indent YAML list items under their parent keys."""

import re


def indent_yaml_lists(content):
    """
    Transform YAML so list items are indented under their parent key.

    Before:
        environment:
        - FOO=bar
        volumes:
        - /data:/data

    After:
        environment:
          - FOO=bar
        volumes:
          - /data:/data

    Also handles list items that are dicts:
    Before:
        configs:
        - source: test
          target: /etc/test

    After:
        configs:
          - source: test
            target: /etc/test
    """
    lines = content.split('\n')
    result = []
    in_list_block = False
    list_base_indent = 0

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        current_indent = len(line) - len(stripped)

        # Check if previous line was a key ending with : (start of potential list)
        if result and not in_list_block:
            prev_stripped = result[-1].strip()
            if prev_stripped.endswith(':') and not prev_stripped.endswith('::'):
                prev_indent = len(result[-1]) - len(result[-1].lstrip())
                # If this line is a list item at the same indent level
                if stripped.startswith('- ') and current_indent == prev_indent:
                    in_list_block = True
                    list_base_indent = prev_indent

        if in_list_block:
            # Check if we've left the list block
            if stripped and not stripped.startswith('- ') and current_indent <= list_base_indent:
                in_list_block = False
                result.append(line)
            elif stripped.startswith('- ') and current_indent == list_base_indent:
                # List item - add 2 spaces
                result.append(' ' * (list_base_indent + 2) + stripped)
            elif current_indent == list_base_indent and stripped:
                # Continuation of list item dict - add 2 spaces
                result.append(' ' * (list_base_indent + 2) + stripped)
            elif not stripped:
                # Empty line
                result.append(line)
                in_list_block = False
            else:
                # Nested content - add 2 spaces
                result.append('  ' + line)
        else:
            result.append(line)

    return '\n'.join(result)


class FilterModule:
    """Ansible filter plugin."""

    def filters(self):
        return {
            'indent_yaml_lists': indent_yaml_lists,
        }
