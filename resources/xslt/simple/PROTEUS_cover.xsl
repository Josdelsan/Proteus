<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- PROTEUS_cover.xsl -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:proteus="http://proteus.lsi.us.es">
    <xsl:template name="document_cover">

        <div id="document_cover">
    
    
            <div id="project_name">
                <xsl:value-of select="properties/stringProperty[@name='name']"/>
            </div>
    
            <div id="document_logo">
                <img alt="Universidad de Sevilla" src="https://cdn.jsdelivr.net/gh/amador-duran-toro/rem/assets/images/logo_us.gif"/>
            </div>
    
            <div id="document_name">
                <xsl:apply-templates select="properties/stringProperty[@name='name']"/>
            </div>
    
            <div id="document_version">
                <xsl:text>Version</xsl:text>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/stringProperty[@name='version']"/>
            </div>
    
            <div id="document_date">
                <xsl:text>Date</xsl:text>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/dateProperty[@name='date']"/>
            </div>
    
    
            <div id="document_prepared_by">
                <xsl:text>Author</xsl:text>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/stringProperty[@name='author']"/>
            </div>
    
        </div>
    
    </xsl:template>
</xsl:stylesheet>