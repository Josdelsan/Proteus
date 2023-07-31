<?xml version="1.0" encoding="utf-8"?>
<!-- EXAMPLE_default.xsl -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:proteus="http://proteus.lsi.us.es">
    <xsl:template name="document_cover">

        <div id="document_cover">
    
            <div id="document_name">
                <xsl:apply-templates select="properties/stringProperty[@name='name']"/>
            </div>

        </div>
    
    </xsl:template>
</xsl:stylesheet>