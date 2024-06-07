<?xml version="1.0" encoding="utf-8"?>



<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>

    <!-- Output -->
    <xsl:output method="html"
        doctype-public="XSLT-compat"
        omit-xml-declaration="yes"
        encoding="iso-8859-1"
        indent="yes"
    />

    <!-- Template includes -->
    <xsl:include href="PROTEUS_utilities.xsl" />
    <xsl:include href="PROTEUS_properties.xsl" />
    <xsl:include href="DOCUMENT_cover.xsl" />
    <xsl:include href="DOCUMENT_document.xsl" />
    <xsl:include href="PROTEUS_section.xsl" />
    <xsl:include href="PROTEUS_paragraph.xsl" />
    <xsl:include href="PROTEUS_glossary_item.xsl" />
    <xsl:include href="PROTEUS_graphic_file.xsl" />
    <xsl:include href="PROTEUS_external_resource.xsl" />
    <xsl:include href="PROTEUS_default.xsl" />
    <xsl:include href="PROTEUS_archetype_link.xsl" />
    

    <xsl:template match="project">
        <xsl:variable name="currentDocumentId" select="proteus-utils:current_document()"/>
        <xsl:for-each select="documents">
            <xsl:if test="object[@id=$currentDocumentId]">
                <xsl:apply-templates select="object[@id=$currentDocumentId]"/>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>