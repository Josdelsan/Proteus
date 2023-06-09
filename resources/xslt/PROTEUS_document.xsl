<?xml version="1.0" encoding="ISO-8859-1"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_document.xsl                           -->
<!-- Content : PROTEUS XSLT for subjects at US - main file    -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->


<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:proteus="http://proteus.lsi.us.es">
    <!-- Match the root object of the document -->
    <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes" />
    <xsl:template match="object[@classes=':Proteus-document']">
        <!-- <!doctype html> -->
        <html>
            <head>
                <meta charset="iso-8859-1"/>
                <meta name="generatedBy" content="PROTEUS"/>
                
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/amador-duran-toro/remus/assets/stylesheets/remus.css"/>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/amador-duran-toro/remus/assets/stylesheets/madeja.css"/>
                
                <title>
                    <xsl:value-of select="properties/stringProperty[@name='name']"/>
                    <xsl:text> </xsl:text>
                 </title>
            </head>
            <body>
                <!-- Cover -->
                <xsl:call-template name="document_cover"/>

                <xsl:call-template name="pagebreak"/>
                
                <!-- Table of contents -->
                <nav id="toc" role="navigation">
                    <h1>Index</h1>
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