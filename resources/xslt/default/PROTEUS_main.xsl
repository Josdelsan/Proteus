<?xml version="1.0" encoding="utf-8"?>

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
    <!-- <xsl:include href="PROTEUS_style.xsl" /> -->
    <xsl:include href="PROTEUS_cover.xsl" />
    <xsl:include href="PROTEUS_utilities.xsl" />
    <xsl:include href="PROTEUS_section.xsl" />
    <xsl:include href="PROTEUS_document.xsl" />
    <xsl:include href="PROTEUS_paragraph.xsl" />
    <xsl:include href="PROTEUS_actor.xsl" />
    <xsl:include href="PROTEUS_graphic_file.xsl" />
    <xsl:include href="PROTEUS_external_resource.xsl" />
    <xsl:include href="PROTEUS_default.xsl" />
    <xsl:include href="PROTEUS_information_requirement.xsl" />
    <xsl:include href="PROTEUS_objective.xsl" />
    <xsl:include href="PROTEUS_use_case.xsl" />
    <xsl:include href="PROTEUS_constraint.xsl" />
    <xsl:include href="PROTEUS_functional_requirement.xsl" />
    <xsl:include href="PROTEUS_nonfunctional_requirement.xsl" />
    <xsl:include href="PROTEUS_organization.xsl" />
    <xsl:include href="PROTEUS_stakeholder.xsl" />

</xsl:stylesheet>