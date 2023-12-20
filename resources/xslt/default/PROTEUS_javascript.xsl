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
    exclude-result-prefixes="proteus"
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
            var channelObject = null;
            window.onload = function()
            {
                console.error("PROTEUS_XSLT: Loading QWebChannel...")
                try {
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        channelObject = channel.objects.channelObject;
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
                    channelObject.open_properties_dialog(id);
                    event.stopPropagation();
                }
            }
        </script>

        <!-- ============================================= -->
        <!-- handleOnClick                                 -->
        <!-- ============================================= -->
        <script>
            function selectAndNavigate(id, event) {
                if (id == "" || id == null) {
                    console.error("PROTEUS_XSLT: " + "HandleOnClick received an empty Id, propagating event to parent.");
                } else {
                    console.error("PROTEUS_XSLT: " + "Clicked on element with Id " + id)
                    channelObject.select_and_navigate_to_object(id);
                    event.stopPropagation();
                }
            }
        </script>

        <!-- ============================================= -->
        <!-- suscribeOnClickHandlers                       -->
        <!-- ============================================= -->
        <!-- Suscribes all elements with a proteus-id      -->
        <script>
            function suscribeOnClickHandlers() {
                const elements = document.querySelectorAll('*[data-proteus-id]');
                elements.forEach(element => {
                    element.addEventListener('dblclick', function(event) {
                        propertiesDialog(element.getAttribute('data-proteus-id'), event);
                    });
                });
            }

            <!-- Function call on load -->
            document.addEventListener('DOMContentLoaded', function () {
                suscribeOnClickHandlers();
            });
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

            <!-- Function call on load -->
            document.addEventListener('DOMContentLoaded', function () {
                removeIdsInsideSymbolicLink();
            });

        </script>

    </xsl:template>
</xsl:stylesheet>
