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

                <!-- Category (enum property) -->
                <xsl:variable name="category_key" select="properties/enumProperty[@name='category']"/>
                <xsl:variable name="category_value">
                    <xsl:call-template name="enum_value">
                        <xsl:with-param name="key" select="$category_key"/>
                    </xsl:call-template>                    
                </xsl:variable>

                <xsl:call-template name="generate_property_row">
                    <xsl:with-param name="label" select="$proteus:lang_category"/>
                    <xsl:with-param name="content" select="$category_value"/>
                    <xsl:with-param name="mandatory" select="true()"/>                    
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
