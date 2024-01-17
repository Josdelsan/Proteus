// =========================================================================
// File        : proteus.js
// Description : Javascript functions for Proteus XSLT                      
// Date        : 16/01/2024            
// Version     : 0.1                    
// Author      : José María Delgado Sánchez
// =========================================================================
// NOTE: console.error is used because logs are not shown in python console,
//       this is for debugging purposes only.

// -----------------------------------------------------------------------
// QWebChannel objects declaration and loading
// -----------------------------------------------------------------------

// DocumentInteraction object to access python functionalities
var documentInteractions = null;

// QWebChannel loading
function loadWebChannel() {
    console.error("PROTEUS_XSLT: Loading QWebChannel...")
    try {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            documentInteractions = channel.objects.documentInteractions;
        });
        console.error("PROTEUS_XSLT: QWebChannel loaded.")
    } catch (error) {
        console.error("PROTEUS_XSLT: " + error.message);
    }
}


// -----------------------------------------------------------------------
// Function    : propertiesDialog
// Description : Open the properties dialog for the element with the given
//               Id. Use documentInteractions object to access python
//               open_properties_dialog method.
// Date        : 16/01/2024
// Version     : 0.1
// Author      : José María Delgado Sánchez
// -----------------------------------------------------------------------
function propertiesDialog(id, event) {
    if (id == "" || id == null) {
        console.error("PROTEUS_XSLT: " + "Doubleclicked on a symbolic linked object with empty Id, propagating event to parent.");
    } else {
        console.error("PROTEUS_XSLT: " + "Doubleclicked on element with Id " + id)
        documentInteractions.open_properties_dialog(id);
        event.stopPropagation();
    }
}


// -----------------------------------------------------------------------
// Function    : selectAndNavigate
// Description : Select the object in the document tree and navigate to
//               it. If the object is not in the current document, ask
//               the user to navigate to the document where the object
//               is located. Use documentInteractions object to access
//               python select_and_navigate_to_object method.
// Date        : 16/01/2024
// Version     : 0.1
// Author      : José María Delgado Sánchez
// -----------------------------------------------------------------------
function selectAndNavigate(id, event) {
    if (id == "" || id == null) {
        console.error("PROTEUS_XSLT: " + "selectAndNavigate received an empty Id, propagating event to parent.");
    } else {
        console.error("PROTEUS_XSLT: " + "Clicked on anchor element with Id " + id)
        documentInteractions.select_and_navigate_to_object(id);
        event.stopPropagation();
    }
}


// -----------------------------------------------------------------------
// Function    : subscribeProteusId
// Description : Subscribe all the elements with data-proteus-id to the
//               necessary events.
// Date        : 16/01/2024
// Version     : 0.1
// Author      : José María Delgado Sánchez
// -----------------------------------------------------------------------
function suscribeProteusId() {
    const elements = document.querySelectorAll('*[data-proteus-id]');
    elements.forEach(element => {

        // propertiesDialog on double click event
        element.addEventListener('dblclick', function (event) {
            propertiesDialog(element.getAttribute('data-proteus-id'), event);
        });

        // TODO: Add more events here if needed
    });
}


// -----------------------------------------------------------------------
// Function    : scrollToElementById
// Description : Scroll the document to the element with the given Id.
// Date        : 16/01/2024
// Version     : 0.1
// Author      : José María Delgado Sánchez
// -----------------------------------------------------------------------
function scrollToElementById(id) {
    if (id == "" || id == null) {
        console.error("PROTEUS_XSLT: " + "Scroll error, cannot scroll to an empty Id.");
        return;
    }

    const element = document.getElementById(id)

    if (element != null) {
        console.error("PROTEUS_XSLT: " + "Scrolling to element with Id " + id)
        element.scrollIntoView({ behavior: "smooth" });
    } else {
        console.error("PROTEUS_XSLT: " + "Scroll error, element with Id " + id + " not found.");
    }
}


// -----------------------------------------------------------------------
// Function    : removeIdsInsideSymbolicLink
// Description : Remove all the Ids of the elements inside a symbolic
//               link. This is necessary because the Ids of the elements
//               inside a symbolic link are going to be duplicated.
// Date        : 16/01/2024
// Version     : 0.1
// Author      : José María Delgado Sánchez
// -----------------------------------------------------------------------
function removeIdsInsideSymbolicLink() {
    const symbolicLinkDivs = document.querySelectorAll('.symbolic-link');
    symbolicLinkDivs.forEach(symbolicLinkDiv => {
        const elementsBelow = symbolicLinkDiv.querySelectorAll('*[id]');
        elementsBelow.forEach(element => {
            element.removeAttribute('id');
        });
    });
}


// -----------------------------------------------------------------------
// Function    : generateTooltip
// Description : Generate tooltips for all the elements with the
//               data-tippy-content attribute. Use tippy.js library.
// Date        : 16/01/2024
// Version     : 0.1
// Author      : José María Delgado Sánchez
// -----------------------------------------------------------------------
function generateTooltip() {
    tippy('[data-tippy-content]', {
        allowHTML: true,
    });
}


// =========================================================================
// Execute code on DOMContentLoaded event
// =========================================================================
document.addEventListener('DOMContentLoaded', function () {
    // Remove Ids to fix HTML code
    removeIdsInsideSymbolicLink();

    // Load QWebChannel
    loadWebChannel();

    // Suscribe all the elements with data-proteus-id to the necessary events
    suscribeProteusId();

    // Generate tooltips
    generateTooltip();
});
