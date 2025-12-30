def _get_chatbot_window_position(bounding_box: dict) -> str:
    """
    Determines chatbot window position in viewport.

    bounding_box must contain:
    - x, y
    - width, height
    - viewport_width, viewport_height
    """

    cx = bounding_box["x"] + bounding_box["width"] / 2
    cy = bounding_box["y"] + bounding_box["height"] / 2

    mid_x = bounding_box["viewport_width"] / 2
    mid_y = bounding_box["viewport_height"] / 2

    if cx < mid_x and cy < mid_y:
        return "top-left"
    if cx >= mid_x and cy < mid_y:
        return "top-right"
    if cx < mid_x and cy >= mid_y:
        return "bottom-left"
    return "bottom-right"


def extract_bounding_box(driver, element):
    rect = driver.execute_script("""
        const r = arguments[0].getBoundingClientRect();
        return {
            x: r.left,
            y: r.top,
            width: r.width,
            height: r.height,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight
        };
    """, element)

    return {k: int(v) for k, v in rect.items()}
