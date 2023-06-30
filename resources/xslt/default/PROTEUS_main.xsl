<?xml version="1.0" encoding="iso-8859-1"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_main.xsl                               -->
<!-- Content : PROTEUS XSLT for subjects at US - main file    -->
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

    <!-- Output -->
    <xsl:output method="html"
        doctype-public="XSLT-compat"
        omit-xml-declaration="yes"
        encoding="iso-8859-1"
        indent="yes"
    />

    <!-- Template includes -->
    <xsl:include href="PROTEUS_cover.xsl" />
    <xsl:include href="PROTEUS_utilities.xsl" />
    <xsl:include href="PROTEUS_section.xsl" />
    <xsl:include href="PROTEUS_document.xsl" />
    <xsl:include href="PROTEUS_paragraph.xsl" />
    <xsl:include href="PROTEUS_actor.xsl" />

</xsl:stylesheet>