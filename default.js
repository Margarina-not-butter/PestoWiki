function _around(wrapTextStart, wrapTextEnd) {
    var activeElement = document.activeElement;
    var start = activeElement.selectionStart;
    var end = activeElement.selectionEnd;
    var selectedText = activeElement.value.substring(start, end);
    
    activeElement.value = activeElement.value.substring(0, start) + wrapTextStart + selectedText + wrapTextEnd + activeElement.value.substring(end);
    if (start === end) {{
        var newCursorPosition = start + wrapTextStart.length;
        activeElement.selectionStart = activeElement.selectionEnd = newCursorPosition;
    }} else {{
        var newCursorPosition = start + wrapTextStart.length + selectedText.length + wrapTextEnd.length;
        activeElement.selectionStart = activeElement.selectionEnd = newCursorPosition;
    }}
}

function _isNumeric(str) {
    if (typeof str != "string") return false
    return !isNaN(str) &&
           !isNaN(parseFloat(str))
}

function _mwHeading(number) {
    eq = "=".repeat(number);
    _around(`${eq} `, ` ${eq}`)
}

function _importJS(address, callback) {
    var script = document.createElement('script');
    script.src = address;
    script.onload = function() {
        if (callback) {
            callback();
        }
    };
    document.head.appendChild(script);
}