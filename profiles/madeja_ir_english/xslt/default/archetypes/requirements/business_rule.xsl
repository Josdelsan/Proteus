<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : business_rule.xsl                              -->
<!-- Content : PROTEUS default XSLT for business-rule         -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/12/02                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->

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
    <!-- business-rule template                        -->
    <!-- ============================================= -->

    <xsl:template match="object[contains(@classes,'business-rule')]">

        <!-- By wrapping both the list and the current property name with commas, -->
        <!-- we ensure we're matching whole names and not partial strings.        -->
        <!-- This was suggested by Claude AI.                                     -->

        <!-- List of excluded properties (not shown) -->
        <xsl:variable name="excluded_properties">,:Proteus-code,:Proteus-name,:Proteus-date,version,dependencies,</xsl:variable>

        <!-- List of mandatory properties (shown even if they are empty)-->
        <xsl:variable name="mandatory_properties">description</xsl:variable>

        <div id="{@id}" data-proteus-id="{@id}">
            <table class="business_rule remus_table">
                <!-- Header -->
                <xsl:call-template name="generate_header">
                    <xsl:with-param name="label"   select="properties/*[@name=':Proteus-code']"/>
                    <xsl:with-param name="class"   select="'business-rule'"/>
                </xsl:call-template>

                <!-- Version row -->
                <xsl:call-template name="generate_version_row"/>

                <!-- Generate rows for all other properties                            -->
                <!-- Each property can be accessed as current() in the called template -->
                <xsl:for-each select="properties/*[not(contains($excluded_properties,concat(',', @name, ',')))]">
                    <xsl:call-template name="generate_property_row">
                        <xsl:with-param name="mandatory" select="contains($mandatory_properties,concat(',', current()/@name, ','))"/>
                    </xsl:call-template>
                </xsl:for-each>
            </table>
        </div>
    </xsl:template>

</xsl:stylesheet>
