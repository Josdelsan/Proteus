<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_javascript.xsl                         -->
<!-- Content : PROTEUS XSLT for subjects at US - javascript   -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/12/20                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>

    <!-- ============================================= -->
    <!-- javascript functions                          -->
    <!-- ============================================= -->

    <xsl:template name="javascript">


        <!-- ============================================= -->
        <!-- QWebChannel specific objects declaration      -->
        <!-- ============================================= -->
        <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script type="text/javascript"> 
            var documentInteractions = null;
            function loadWebChannel()
            {
                console.error("PROTEUS_XSLT: Loading QWebChannel...")
                try {
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        documentInteractions = channel.objects.documentInteractions;
                    });
                    console.error("PROTEUS_XSLT: QWebChannel loaded.")
                } catch (error) {
                    console.error("PROTEUS_XSLT: " + error.message);
                }
            }
        </script>

        <!-- ============================================= -->
        <!-- propertiesDialog                              -->
        <!-- ============================================= -->
        <!-- Handles double click event in object to open  -->
        <!-- properties dialog.                            -->
        <script>
            function propertiesDialog(id, event) {
                if (id == "" || id == null) {
                    console.error("PROTEUS_XSLT: " + "Doubleclicked on a symbolic linked object with empty Id, propagating event to parent.");
                } else {
                    console.error("PROTEUS_XSLT: " + "Doubleclicked on element with Id " + id)
                    documentInteractions.open_properties_dialog(id);
                    event.stopPropagation();
                }
            }
        </script>

        <!-- ============================================= -->
        <!-- selectAndNavigate                             -->
        <!-- ============================================= -->
        <!-- Handles clicks on anchor elements that are    -->
        <!-- links to other objects.                       -->
        <script>
            function selectAndNavigate(id, event) {
                if (id == "" || id == null) {
                    console.error("PROTEUS_XSLT: " + "selectAndNavigate received an empty Id, propagating event to parent.");
                } else {
                    console.error("PROTEUS_XSLT: " + "Clicked on anchor element with Id " + id)
                    documentInteractions.select_and_navigate_to_object(id);
                    event.stopPropagation();
                }
            }
        </script>

        <!-- ============================================= -->
        <!-- suscribeProteusId                       -->
        <!-- ============================================= -->
        <!-- Suscribes all elements with a proteus-id      -->
        <script>
            function suscribeProteusId() {
                const elements = document.querySelectorAll('*[data-proteus-id]');
                elements.forEach(element => {
                    element.addEventListener('dblclick', function(event) {
                        propertiesDialog(element.getAttribute('data-proteus-id'), event);
                    });
                });
            }
        </script>

        <!-- ============================================= -->
        <!-- scrollToElementById                           -->
        <!-- ============================================= -->
        <!-- Scrolls to the element with the given Id.     -->
        <!-- Avoid scrolling to a symlinked object.        -->
        <!-- This is the default scroll function  -->
        <script>
            function scrollToElementById(id) {
                if (id == "" || id == null) {
                    console.error("PROTEUS_XSLT: " + "Scroll error, cannot scroll to an empty Id.");
                    return;
                }

                const element = document.getElementById(id)

                if (element != null) {
                    console.error("PROTEUS_XSLT: " + "Scrolling to element with Id " + id)
                    element.scrollIntoView( {behavior: "smooth"} );
                } else {
                    console.error("PROTEUS_XSLT: " + "Scroll error, element with Id " + id + " not found.");
                }
            }
        </script>


        <!-- ============================================= -->
        <!-- removeIdsInsideSymbolicLink                   -->
        <!-- ============================================= -->
        <!-- Removes all Ids inside a symbolic link.       -->
        <!-- This is done to avoid id duplication.         -->
        <script>
            function removeIdsInsideSymbolicLink() {
                const symbolicLinkDivs = document.querySelectorAll('.symbolic-link');
                symbolicLinkDivs.forEach(symbolicLinkDiv => {
                    const elementsBelow = symbolicLinkDiv.querySelectorAll('*[id]');
                        elementsBelow.forEach(element => {
                        element.removeAttribute('id');
                        });
                    });
            }
        </script>


        <!-- ============================================= -->
        <!-- generateTooltip                               -->
        <!-- ============================================= -->
        <!-- Generates tooltips for all elements with a     -->
        <!-- data-tippy-content attribute.                  -->
        <!-- Tooltips are generated using tippy v6 library -->
        <!-- https://atomiks.github.io/tippyjs/v6/getting-started/ -->
        <script>
            function generateTooltip() {
                tippy('[data-tippy-content]',{
                    allowHTML: true,
                });
            }
        </script>


        <!-- ============================================= -->
        <!-- Function call on load                         -->
        <!-- ============================================= -->
        <script>
            <!-- Function call on load -->
            document.addEventListener('DOMContentLoaded', function () {
                removeIdsInsideSymbolicLink();
                loadWebChannel();
                suscribeProteusId();
                generateTooltip();
            });
        </script>

    </xsl:template>
</xsl:stylesheet>
