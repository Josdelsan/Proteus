<?xml version="1.0" encoding="ISO-8859-1"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_cover.xsl                              -->
<!-- Content : PROTEUS XSLT for subjects at US - cover        -->
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
    <xsl:template name="document_cover">

        <div id="document_cover">
            <a id="{@id}"></a>
    
            <div id="project_name">
                <xsl:value-of select="$proteus:lang_project"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/stringProperty[@name='name']"/>
            </div>
    
            <div id="document_logo">
                <img alt="Universidad de Sevilla" src="https://cdn.jsdelivr.net/gh/amador-duran-toro/rem/assets/images/logo_us.gif"/>
            </div>
    
            <div id="document_name">
                <xsl:apply-templates select="properties/stringProperty[@name='name']"/>
            </div>
    
            <div id="document_version">
                <xsl:value-of select="$proteus:lang_version"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/stringProperty[@name='version']"/>
            </div>
    
            <div id="document_date">
                <xsl:value-of select="$proteus:lang_date"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/dateProperty[@name='date']"/>
            </div>
    
    
            <div id="document_prepared_by">
                <xsl:value-of select="$proteus:lang_prepared_by"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/stringProperty[@name='author']"/>
            </div>
    
        </div>
    
    </xsl:template>
</xsl:stylesheet>