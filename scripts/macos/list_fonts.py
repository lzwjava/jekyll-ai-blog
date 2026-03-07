from CoreText import (
    CTFontManagerCopyAvailableFontDescriptors,
    CTFontDescriptorCopyAttribute,
    kCTFontNameAttribute,
)


def list_fonts():
    # Get all font descriptors
    font_descriptors = CTFontManagerCopyAvailableFontDescriptors()

    # Set to store unique font names
    font_names = set()

    for descriptor in font_descriptors:
        # Get the PostScript name of the font
        font_name = CTFontDescriptorCopyAttribute(descriptor, kCTFontNameAttribute)
        if font_name:
            font_names.add(str(font_name))

    # Sort and print the font names
    for name in sorted(font_names):
        print(name)


if __name__ == "__main__":
    try:
        list_fonts()
    except Exception as e:
        print(f"Error: {e}")
