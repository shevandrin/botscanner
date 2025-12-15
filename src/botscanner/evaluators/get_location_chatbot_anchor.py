def get_location_chatbot_anchor(driver, element):
    """
    Determine where an element is located in the viewport.
    
    Returns:
        str: one of
            - 'top-left'
            - 'top-right'
            - 'bottom-left'
            - 'bottom-right'
    """

    # element position and size
    location = element.location_once_scrolled_into_view
    size = element.size

    element_center_x = location["x"] + size["width"] / 2
    element_center_y = location["y"] + size["height"] / 2

    # viewport size
    viewport_width = driver.execute_script("return window.innerWidth;")
    viewport_height = driver.execute_script("return window.innerHeight;")

    horizontal = "left" if element_center_x < viewport_width / 2 else "right"
    vertical = "top" if element_center_y < viewport_height / 2 else "bottom"

    return f"{vertical}-{horizontal}"