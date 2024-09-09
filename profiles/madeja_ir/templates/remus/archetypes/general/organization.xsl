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

                <!-- Address -->
                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label"     select="$proteus:lang_address"/>
                    <xsl:with-param name="content"   select="properties/stringProperty[@name='address']"/>
                    <xsl:with-param name="mandatory" select="true()"/>
                </xsl:call-template>

                <!-- phone-number -->
                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label"     select="$proteus:lang_telephone"/>
                    <xsl:with-param name="content"   select="properties/stringProperty[@name='phone-number']"/>
                </xsl:call-template>

                <!-- web -->
                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label"     select="$proteus:lang_web"/>
                    <xsl:with-param name="content"   select="properties/stringProperty[@name='web']"/>
                </xsl:call-template>

                <!-- Comments -->
                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label"   select="$proteus:lang_comments"/>
                    <xsl:with-param name="content" select="properties/markdownProperty[@name='comments']"/>
                </xsl:call-template>

            </table>
        </div>
    </xsl:template>

</xsl:stylesheet>
