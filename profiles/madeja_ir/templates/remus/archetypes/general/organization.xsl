<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : organization.xsl                               -->
<!-- Content : PROTEUS default XSLT organization              -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/12/07                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/09 (Amador Durán)                      -->
<!-- match must be object[ends-with(@classes,'organization')] -->
<!-- To check if an object is of a given class:               -->
<!--    object[contains(@classes,class_name)]                 -->
<!-- To check if an object is of a given final class:         -->
<!--    object[ends-with(@classes,class_name)]                -->
<!-- PROBLEM: XSLT 1.0 does not include ends-with             -->
<!-- archetype-link -> symbolic-link                          -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/13 (Amador Durán)                      -->
<!-- Review after integration of trace properties in the list -->
<!-- of properties.                                           -->
<!-- Use a parametrized template to iterate over the ordinary -->
<!-- properties and generate a row for each them in a similar -->
<!-- way to the default template.                             -->
<!-- ======================================================== -->

<!-- TODO: how can we know if a property is mandatory?        -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>
    <!-- ============================================= -->
    <!-- organization template                         -->
    <!-- ============================================= -->

    <xsl:template match="object[contains(@classes,'organization')]">
        <div id="{@id}" data-proteus-id="{@id}">
            <table class="organization remus_table">

                <!-- Header-->
                <xsl:call-template name="generate_header">
                    <xsl:with-param name="label"   select="$proteus:lang_organization"/>
                    <xsl:with-param name="class"   select="'organization'"/>
                </xsl:call-template>

                <xsl:variable name="excluded_properties">:Proteus-name,:Proteus-date,version</xsl:variable>
                <xsl:variable name="mandatory_properties">address</xsl:variable>

                <!-- Generate rows for all ordinary properties -->
                <xsl:for-each select="properties/*[not(contains($excluded_properties,@name))]">
                    <xsl:call-template name="generate_property_row">
                        <xsl:with-param name="label"     select="$property_labels/label[@key = current()/@name]"/>
                        <xsl:with-param name="content"   select="."/>
                        <xsl:with-param name="mandatory" select="contains($mandatory_properties,current()/@name)"/>
                    </xsl:call-template>
                </xsl:for-each>

            </table>
        </div>
    </xsl:template>

</xsl:stylesheet>
