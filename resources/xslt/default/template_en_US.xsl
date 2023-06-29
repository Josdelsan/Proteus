<?xml version="1.0" encoding="ISO-8859-1"?>

<!-- ========================================================= -->
<!-- File    : template_en_US.xsl                              -->
<!-- Content : PROTEUS XSLT for subjects at US - Spanish main  -->
<!--           file                                            -->
<!-- Author  : Amador Durán Toro                               -->
<!--           José María Delgado Sánchez                      -->
<!-- Date    : 2023/06/29                                      -->
<!-- Version : 1.0                                             -->
<!-- ========================================================= -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    exclude-result-prefixes="proteus"
>

<!-- ======================================================== -->
<!-- Import default localized strings                         -->
<!-- ======================================================== -->

<xsl:import href="PROTEUS_i18n_English.xsl"/>

<!-- ======================================================== -->
<!-- Localized PROTEUS-specific strings                       -->
<!-- ======================================================== -->

<xsl:variable name="proteus:lang">en</xsl:variable>
<xsl:variable name="proteus:lang_part">Part</xsl:variable>
<xsl:variable name="proteus:lang_warnings">Warnings</xsl:variable>
<xsl:variable name="proteus:lang_abstract">abstract</xsl:variable>
<xsl:variable name="proteus:lang_TBD_expanded">To Be Determined</xsl:variable>

<!-- ======================================================== -->
<!-- Include main XSLT file                                   -->
<!-- ======================================================== -->

<xsl:include href="PROTEUS_main.xsl"/>

</xsl:stylesheet>
