<?xml version="1.0" encoding="utf-8"?>
<!-- EXAMPLE_main.xsl -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:proteus="http://proteus.lsi.us.es">
    <!-- Output -->
    <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes" />

    <!-- Template includes -->
    <xsl:include href="EXAMPLE_cover.xsl"/>
    <xsl:include href="EXAMPLE_utilities.xsl"/>
    <xsl:include href="EXAMPLE_section.xsl"/>
    <xsl:include href="EXAMPLE_document.xsl"/>
    <xsl:include href="EXAMPLE_default.xsl"/>

</xsl:stylesheet>