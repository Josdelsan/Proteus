<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.lsi.us.es">
    <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes"
        encoding="UTF-8" indent="yes" />
    <xsl:template match="project">
        <!-- <!doctype html> -->
        <html>
            <head>
                <meta charset="utf-8" />
                <meta name="generatedBy" content="PROTEUS" />

                <title>
                    <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']" />
                    <xsl:text> </xsl:text>
                </title>

                <style>
                    p.figure_caption,
                    p.matrix_caption {
                    margin-top: 4px;
                    }

                    span.figure_caption_label,
                    span.matrix_caption_label {
                    font-weight: bold;
                    }
                    div.figure {
                    text-align: center;
                    }
                </style>

            </head>
            <body>
                <!-- Cover -->
                <div id="document_cover" style="text-align: center;">
                    <h1>
                        <strong>
                            <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']" />
                            <xsl:text> figures</xsl:text>
                        </strong>
                    </h1>
                </div>

                <xsl:apply-templates select="documents/object" />

            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>