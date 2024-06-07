// =========================================================================
// File        : proteus.js
// Description : Javascript functions for Proteus XSLT                      
// Date        : 16/01/2024            
// Version     : 0.1                    
// Author      : José María Delgado Sánchez
// =========================================================================
// NOTE: console.error is used because logs are not shown in python console,
//       this is for debugging purposes only.
// =========================================================================

// Constants
const PROTEUS_XSLT_VERSION = "0.1";
const PROTEUS_XSLT_NAME = "Proteus XSLT";
const PROTEUS_XSLT_LOG_PREFIX = `${PROTEUS_XSLT_NAME}:${PROTEUS_XSLT_VERSION} - `;

// WebChannel objects
var proteusBasics = null;


// -----------------------------------------------------------------------
// Custom log function
// -----------------------------------------------------------------------
function log(message) {
    console.log(PROTEUS_XSLT_LOG_PREFIX + message);
}

// -----------------------------------------------------------------------
// QWebChannel loading
// -----------------------------------------------------------------------

// NOTE: This function is used to interact with Python code, if you are
//       using this script outside PROTEUS application, you can remove
//       this function to prevent errors.
function loadWebChannel() {
    try {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            proteusBasics = channel.objects.proteusBasics;

            // Scroll to the current object as soon as the QWebChannel is loaded
            // This improves user experience when the document has a lot of
            // resources (images, stylesheets, etc.)
            proteusBasics.get_current_object_id(function (oid) {
                onTreeObjectSelected(oid);
            });

            log("QWebChannel loaded.")
        });
    } catch (error) {
        console.error(error.message);
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
// NOTE: This function is used to interact with Python code, if you are
//       using this script outside PROTEUS application, you can remove
//       this function to prevent errors.
function suscribeProteusId() {
    const elements = document.querySelectorAll('*[data-proteus-id]');
    elements.forEach(element => {

        // propertiesDialog on double click event
        element.addEventListener('dblclick', function (event) {
            propertiesDialog(element.getAttribute('data-proteus-id'), event);
        });

        // NOTE: Add more events here if needed
    });
}


// -----------------------------------------------------------------------
// Function    : onTreeObjectSelected
// Description : Scroll the document to the element with the given Id.
// Date        : 16/01/2024
// Version     : 0.1
// Author      : José María Delgado Sánchez
// -----------------------------------------------------------------------
// NOTE: This function is used to interact with Python code, if you are
//       using this script outside PROTEUS application, you can remove
//       this function to prevent errors.
function onTreeObjectSelected(id) {
    if (id == "" || id == null) {
        log("Scroll error, cannot scroll to an empty Id.");
        return;
    }

    const element = document.getElementById(id)

    if (element != null) {
        log("Scrolling to element with Id " + id)
        element.scrollIntoView({ behavior: "smooth" });
    } else {
        log("Scroll error, element with Id " + id + " not found.");
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
    
});

// =========================================================================
// Execute code on load event
// =========================================================================
window.onload = function () {

};
