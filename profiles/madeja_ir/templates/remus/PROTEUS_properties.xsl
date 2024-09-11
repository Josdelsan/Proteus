<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_properties.xsl                         -->
<!-- Content : PROTEUS default XSLT for properties            -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/12/08                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/11 (Amador Durán)                      -->
<!-- new template for urlProperty                             -->
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
        <ul class="stakeholders">
            <xsl:for-each select="trace">
                <xsl:variable name="targetId" select="@target" />
                <xsl:variable name="targetObject" select="//object[@id = $targetId]" />

                <xsl:if test="$targetObject">
                    <li>
                        <a href="#{$targetId}" onclick="selectAndNavigate(`{$targetId}`, event)">
                            <xsl:value-of select="$targetObject/properties/stringProperty[@name = ':Proteus-name']" />
                        </a>
                    </li>
                </xsl:if>
            </xsl:for-each>
        </ul>
    </xsl:template>

    <!-- Paragraph mode -->
    <xsl:template match="traceProperty" mode="paragraph">
        <xsl:for-each select="trace">
            <xsl:variable name="targetId" select="@target" />
            <xsl:variable name="targetObject" select="//object[@id = $targetId]" />

            <xsl:if test="$targetObject">
                <p>
                    <a href="#{$targetId}" onclick="selectAndNavigate(`{$targetId}`, event)">
                        <xsl:value-of select="$targetObject/properties/stringProperty[@name = ':Proteus-name']" />
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

</xsl:stylesheet>