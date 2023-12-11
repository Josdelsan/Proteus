<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_document.xsl                           -->
<!-- Content : PROTEUS XSLT for subjects at US - document     -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
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
    <!-- Match the root object of the document -->
    <xsl:template match="object[@classes=':Proteus-document']">
        <!-- <!doctype html> -->
        <html>
            <head>
                <meta charset="utf-8"/>
                <meta name="generatedBy" content="PROTEUS"/>
                
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/amador-duran-toro/remus/assets/stylesheets/remus.css"/>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/amador-duran-toro/remus/assets/stylesheets/madeja.css"/>
                
                <title>
                    <xsl:value-of select="$proteus:lang_project"/>
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="parent::*/parent::*/properties/stringProperty[@name=':Proteus-name']"/>
                 </title>
                 
                <!-- <xsl:call-template name="style"/> -->

                <style>
                    @media print {
                        .page-break {
                          clear: both;
                          page-break-before: always;
                        }
                      }
        
                      table {
                        width: 98%;
                        margin: 0 auto;
                        margin-bottom: 2em;
                        border: 1px solid black;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                    }
                </style>

                <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
                <script type="text/javascript">

                    var channelObject = null;
                    window.onload = function()
                    {
                        try {
                            new QWebChannel(qt.webChannelTransport, function(channel) {
                                channelObject = channel.objects.channelObject;
                            });
                        } catch (error) {
                            console.error(error.message);
                        }
                    }
                </script>
                <script>
                        function handleDoubleClick(event) {
                            var clickedElement = event.target;
                            var closestProteusArea = clickedElement.closest('.proteus-area');
                            var id = closestProteusArea.id;

                            if (id == "" || id == null) {
                                console.error("No id found in clicked element");
                            } else {
                                channelObject.open_properties_dialog(id);
                            }
                        }

                        document.addEventListener('DOMContentLoaded', function () {
                            var proteusElements = document.querySelectorAll('.proteus-area');
                            proteusElements.forEach(function (element) {
                                element.addEventListener('dblclick', handleDoubleClick);
                            });
                        });
                </script>
            </head>
            <body>
                <!-- Cover -->
                <xsl:call-template name="document_cover"/>

                <xsl:call-template name="pagebreak"/>
                
                <!-- Table of contents -->
                <nav id="toc" role="navigation">
                    <h1><xsl:value-of select="$proteus:lang_TOC"/></h1>
                    <ul class="toc_list toc_list_level_1">
                        <xsl:apply-templates select="children/object[@classes='section']" mode="toc"/>
                    </ul>
                </nav>

                <xsl:call-template name="pagebreak"/>

                <!-- Document body -->
                <xsl:apply-templates select="children/object"/>


            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>