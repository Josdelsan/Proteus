<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : stakeholder.xsl                                -->
<!-- Content : PROTEUS default XSLT for stakeholder           -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/07                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/09 (Amador Durán)                      -->
<!-- match must be object[ends-with(@classes,'stakeholder')]  -->
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
    xmlns:ext="http://exslt.org/common"
    extension-element-prefixes="ext"
>
    <!-- ============================================= -->
    <!-- stakeholder template                          -->
    <!-- ============================================= -->

    <xsl:template match="object[contains(@classes,'stakeholder')]">

        <div id="{@id}" data-proteus-id="{@id}">
            <table class="stakeholder remus_table">

                <!-- Header -->
                <xsl:call-template name="generate_header">
                    <xsl:with-param name="label" select="$proteus:lang_stakeholder"/>
                    <xsl:with-param name="class" select="'stakeholder'"/>
                </xsl:call-template>

                <!-- Organization -->
                <xsl:variable name="organization_content" select="traces/traceProperty[@name='works-for']" />
                <xsl:choose>
                    <xsl:when test="$organization_content/trace">
                        <xsl:call-template name="generate_trace_row">
                            <xsl:with-param name="label"   select="$proteus:lang_organization"/>
                            <xsl:with-param name="content" select="$organization_content"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <tr>
                            <th><xsl:value-of select="$proteus:lang_organization"/></th>
                            <td>
                                <span><xsl:value-of select="$proteus:lang_freelance"/></span>
                            </td>
                        </tr>
                    </xsl:otherwise>
                </xsl:choose>

                <!-- Role -->
                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label"     select="$proteus:lang_role"/>
                    <xsl:with-param name="content"   select="properties/stringProperty[@name='role']"/>
                    <xsl:with-param name="mandatory" select="true()"/>
                </xsl:call-template>

                <!-- Category -->
                <xsl:variable name="category" select="properties/enumProperty[@name='category']"/>
                <xsl:variable name="diccionario" select="$proteus:enum_dict" as="node()"/>
                <tr>Categoría = "<xsl:value-of select="$category"/>" (<xsl:value-of select="$category/text()"/>)</tr>
                <tr>Enum = "<xsl:value-of select="$diccionario"/>" </tr>
                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label" select="$proteus:lang_category"/>
                    <!-- <xsl:with-param name="content" select="key('enum-dict', properties/enumProperty[@name='category'])"/> -->
                    <!-- <xsl:with-param name="content" select="properties/enumProperty[@name='category']"/> -->
                    <!-- <xsl:with-param name="content" select="$proteus:enum_dict/enum[@name=$category]/text()"/> -->
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
