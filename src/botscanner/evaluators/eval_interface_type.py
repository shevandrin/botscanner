from bs4 import BeautifulSoup
import re


def _evaluate_interface_type(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    text_blob = html.lower()

    if any(token in text_blob for token in [
        "100vh", "100vw", "fullscreen", "full-screen"
    ]):
        return "fullscreen"

    modal_roles = {"dialog", "alertdialog"}
    for el in soup.find_all(True):
        role = el.get("role")
        cls = " ".join(el.get("class", [])).lower()

        if role in modal_roles:
            return "modal"

        if any(k in cls for k in ["modal", "dialog", "overlay", "backdrop"]):
            return "modal"

    for el in soup.find_all(True):
        style = (el.get("style") or "").lower()
        cls = " ".join(el.get("class", [])).lower()

        if "position:fixed" in style or "position: absolute" in style:
            if any(k in cls for k in ["chat", "popup", "widget", "bubble"]):
                return "popup"

    return "embedded"