<?xml version="1.0" encoding="utf-8"?>
<!-- EXAMPLE_document.xsl -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:proteus="http://proteus.lsi.us.es">
    <!-- Match the root object of the document -->
    <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes" />
    <xsl:template match="object[@classes=':Proteus-document']">
        <!-- <!doctype html> -->
        <html>
            <head>
                <meta charset="utf-8"/>
                <meta name="generatedBy" content="PROTEUS"/>
                
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/amador-duran-toro/remus/assets/stylesheets/remus.css"/>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/amador-duran-toro/remus/assets/stylesheets/madeja.css"/>
                
                <title>
                    <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']"/>
                    <xsl:text> </xsl:text>
                 </title>
                 <style>
                    @media print {
                      .page-break {
                        page-break-before: always;
                      }
                    }

                    table {
                        width: 95%;
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
            </head>
            <body>
                <!-- Cover -->
                <xsl:call-template name="document_cover"/>

                <xsl:call-template name="pagebreak"/>

                <!-- Document body -->
                <xsl:apply-templates select="children/object"/>


            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>