#!/usr/bin/env python3
"""
Validation utilities for grammar fixes
"""


def validate_grammar_fix(
    original_content, fixed_content, max_line_diff=2, max_length_change=0.2
):
    """
    Validate that the grammar fix maintains similar structure and length.

    Args:
        original_content (str): The original content
        fixed_content (str): The grammar-fixed content
        max_line_diff (int): Maximum allowed line count difference (default: 2)
        max_length_change (float): Maximum allowed length change as percentage (default: 0.2 = 20%)

    Raises:
        Exception: If validation fails

    Returns:
        bool: True if validation passes
    """
    original_lines = original_content.split("\n")
    fixed_lines = fixed_content.split("\n")

    # Check line count - should be similar (allow some flexibility)
    line_diff = abs(len(original_lines) - len(fixed_lines))
    if line_diff > max_line_diff:
        raise Exception(
            f"Line count changed too much: {len(original_lines)} -> {len(fixed_lines)} (diff: {line_diff})"
        )

    # Check length - should be similar (allow up to specified change)
    original_length = len(original_content)
    fixed_length = len(fixed_content)
    if original_length > 0:  # Avoid division by zero
        length_change = abs(original_length - fixed_length) / original_length
        if length_change > max_length_change:
            raise Exception(
                f"Content length changed too much: {original_length} -> {fixed_length} ({length_change:.1%} change)"
            )

    # Check for unwanted markdown additions
    original_bold_count = original_content.count("**")
    fixed_bold_count = fixed_content.count("**")
    if fixed_bold_count > original_bold_count:
        raise Exception(
            f"AI added unwanted markdown bold syntax: {original_bold_count} -> {fixed_bold_count}"
        )

    original_italic_count = original_content.count("*") - original_bold_count * 2
    fixed_italic_count = fixed_content.count("*") - fixed_bold_count * 2
    if fixed_italic_count > original_italic_count:
        raise Exception("AI added unwanted markdown italic syntax")

    return True


def validate_markdown_syntax(original_content, fixed_content):
    """
    Validate that no unwanted markdown syntax was added.

    Args:
        original_content (str): The original content
        fixed_content (str): The grammar-fixed content

    Raises:
        Exception: If unwanted markdown syntax was added

    Returns:
        bool: True if validation passes
    """
    # Check for bold syntax
    original_bold = original_content.count("**")
    fixed_bold = fixed_content.count("**")
    if fixed_bold > original_bold:
        raise Exception(
            f"Added unwanted bold markdown: {original_bold} -> {fixed_bold}"
        )

    # Check for italic syntax (single asterisks not part of bold)
    original_single_asterisks = original_content.count("*") - (original_bold * 2)
    fixed_single_asterisks = fixed_content.count("*") - (fixed_bold * 2)
    if fixed_single_asterisks > original_single_asterisks:
        raise Exception("Added unwanted italic markdown")

    # Check for other markdown additions
    markdown_patterns = ["`", "#", ">", "|", "[", "]", "(", ")"]
    for pattern in markdown_patterns:
        original_count = original_content.count(pattern)
        fixed_count = fixed_content.count(pattern)
        if fixed_count > original_count * 1.2:  # Allow some flexibility
            raise Exception(
                f"Significant increase in '{pattern}' characters: {original_count} -> {fixed_count}"
            )

    return True


def validate_content_structure(original_content, fixed_content):
    """
    Validate that the content structure is preserved.

    Args:
        original_content (str): The original content
        fixed_content (str): The grammar-fixed content

    Raises:
        Exception: If content structure changed significantly

    Returns:
        bool: True if validation passes
    """
    original_lines = original_content.split("\n")
    fixed_lines = fixed_content.split("\n")

    # Check paragraph structure (empty lines)
    original_empty_lines = len([line for line in original_lines if not line.strip()])
    fixed_empty_lines = len([line for line in fixed_lines if not line.strip()])

    if abs(original_empty_lines - fixed_empty_lines) > 1:
        raise Exception(
            f"Paragraph structure changed: {original_empty_lines} -> {fixed_empty_lines} empty lines"
        )

    # Check for major sentence structure changes
    original_sentences = (
        original_content.count(".")
        + original_content.count("!")
        + original_content.count("?")
    )
    fixed_sentences = (
        fixed_content.count(".") + fixed_content.count("!") + fixed_content.count("?")
    )

    if abs(original_sentences - fixed_sentences) > 2:
        raise Exception(
            f"Sentence structure changed significantly: {original_sentences} -> {fixed_sentences} sentences"
        )

    return True
