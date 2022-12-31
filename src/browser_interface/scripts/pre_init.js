var Module = {
    print: (function () {
        // Overwrite the default print function to print into our textarea
        var element = document.getElementById('program-output');
        if (element) element.innerText = ''; // clear browser cache
        return function (text) {
            if (arguments.length > 1) text = Array.prototype.slice.call(arguments).join(' ');
            // These replacements are necessary if you render to raw HTML
            //text = text.replace(/&/g, "&amp;");
            //text = text.replace(/</g, "&lt;");
            //text = text.replace(/>/g, "&gt;");
            //text = text.replace('\n', '<br>', 'g');
            console.log(text);
            if (element) {
                element.innerText += text + "\n";
            }
        };
    })()
};