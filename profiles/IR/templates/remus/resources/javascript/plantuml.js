// https://plantuml.com/es/code-javascript-synchronous

function encode64(data) {
    r = "";
    for (i = 0; i < data.length; i += 3) {
        if (i + 2 == data.length) {
            r += append3bytes(data.charCodeAt(i), data.charCodeAt(i + 1), 0);
        } else if (i + 1 == data.length) {
            r += append3bytes(data.charCodeAt(i), 0, 0);
        } else {
            r += append3bytes(data.charCodeAt(i), data.charCodeAt(i + 1),
                data.charCodeAt(i + 2));
        }
    }
    return r;
}

function append3bytes(b1, b2, b3) {
    c1 = b1 >> 2;
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4);
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6);
    c4 = b3 & 0x3F;
    r = "";
    r += encode6bit(c1 & 0x3F);
    r += encode6bit(c2 & 0x3F);
    r += encode6bit(c3 & 0x3F);
    r += encode6bit(c4 & 0x3F);
    return r;
}

function encode6bit(b) {
    if (b < 10) {
        return String.fromCharCode(48 + b);
    }
    b -= 10;
    if (b < 26) {
        return String.fromCharCode(65 + b);
    }
    b -= 26;
    if (b < 26) {
        return String.fromCharCode(97 + b);
    }
    b -= 26;
    if (b == 0) {
        return '-';
    }
    if (b == 1) {
        return '_';
    }
    return '?';
}


async function fetchPlantUMLDiagram(plantUMLCode) {
    const plantUMLServerUrl = 'http://www.plantuml.com/plantuml/png/';

    try {
        console.error('PlantUML code ' + plantUMLCode)

        // DEFLATE compression
        const utf8PlantUMLCode = unescape(encodeURIComponent(plantUMLCode));
        const deflatedPlantUMLCode = encode64(deflate(utf8PlantUMLCode, 9));

        console.error('Trying to fetch PlantUML diagram from: ' + plantUMLServerUrl + deflatedPlantUMLCode)
        const response = await fetch(`${plantUMLServerUrl}${deflatedPlantUMLCode}`);

        const blob = await response.blob();
        const base64 = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
        });

        return base64;
    } catch (error) {
        console.error(error);
        return null;
    }
}

async function displayPlantUMLDiagram(plantUMLCode, img_element_id) {
    const base64Diagram = await fetchPlantUMLDiagram(plantUMLCode);
    console.error('Inserting PlantUML diagram into: ' + img_element_id)

    if (base64Diagram) {
        const imgElement = document.getElementById(img_element_id);
        imgElement.src = `data:image/png;base64,${base64Diagram}`;
    } else {
        console.error('Failed to retrieve PlantUML diagram.');
    }
}