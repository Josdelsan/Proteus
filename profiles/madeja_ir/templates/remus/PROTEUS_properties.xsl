<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_properties.xsl                         -->
<!-- Content : PROTEUS default XSLT for properties            -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/12/08                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/11 (Amador Durán)                      -->
<!-- New template for urlProperty                             -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/14 (Amador Durán)                      -->
<!-- Improvements in template for urlProperty.                -->
<!-- New template for enum property.                          -->
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
    <!-- traceProperty                                 -->
    <!-- ============================================= -->

    <!-- List mode -->
    <xsl:template match="traceProperty">
        <ul class="traces">
            <xsl:for-each select="trace">
                <xsl:variable name="target_id" select="@target" />
                <xsl:variable name="target_object" select="//object[@id=$target_id]" />
                <xsl:variable name="target_name" select="$target_object/properties/stringProperty[@name=':Proteus-name']" />                

                <xsl:if test="$target_object">
                    <li>
                        <a href="#{$target_id}" onclick="selectAndNavigate(`{$target_id}`, event)">
                            <xsl:value-of select="$target_name"/>
                        </a>
                    </li>
                </xsl:if>
            </xsl:for-each>
        </ul>
    </xsl:template>

    <!-- Paragraph mode -->
    <xsl:template match="traceProperty" mode="paragraph">
        %%traceProperty <xsl:value-of select="@name"/>%%
        <xsl:for-each select="trace">
            <xsl:variable name="target_id" select="@target" />
            <xsl:variable name="target_object" select="//object[@id=$target_id]" />
            <xsl:variable name="target_name" select="$target_object/properties/stringProperty[@name=':Proteus-name']" />                

            <xsl:if test="$target_object">
                <p>
                    <a href="#{$target_id}" onclick="selectAndNavigate(`{$target_id}`, event)">
                        <xsl:value-of select="$target_name"/>
                    </a>
                </p>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <!-- ============================================= -->
    <!-- markdownProperty                              -->
    <!-- ============================================= -->

    <xsl:template match="markdownProperty">
        <xsl:call-template name="generate_markdown">
            <xsl:with-param name="content" select="."/>
        </xsl:call-template>
    </xsl:template>

    <!-- ============================================= -->
    <!-- urlProperty                                   -->
    <!-- ============================================= -->

    <xsl:template match="urlProperty">
        <xsl:variable name="href" select="."/>
        <a href="{$href}"><xsl:value-of select="$href"/></a>
    </xsl:template>

    <!-- ============================================= -->
    <!-- enumProperty                                  -->
    <!-- ============================================= -->

    <xsl:template match="enumProperty">
        <xsl:value-of select="$enum_labels/label[@key=current()/text()]"/>
    </xsl:template>

</xsl:stylesheet>