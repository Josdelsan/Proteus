<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_paragraph.xsl                          -->
<!-- Content : PROTEUS XSLT for subjects at US - paragraph    -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/07 (Amador Durán)                      -->
<!-- match must be object[ends-with(@classes,'paragraph')]    -->
<!-- since paragraph is a subclass of                         -->
<!-- general-traceable-object.                                -->
<!-- To check if an object is of a given class:               -->
<!--    object[contains(@classes,class_name)]                 -->
<!-- To check if an object is of a given final class:         -->
<!--    object[ends-with(@classes,class_name)]                -->
<!-- PROBLEM: XSLT 1.0 does not include ends-with             -->
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
    <!-- =========================================================== -->
    <!-- paragraph template                                          -->
    <!-- =========================================================== -->

    <xsl:template match="object[contains(@classes,'paragraph')]">
        <div id="{@id}" data-proteus-id="{@id}">
            <xsl:variable name="content" select="properties/markdownProperty[@name='text']"/>
            <xsl:variable name="nonempty_content" select="string-length(normalize-space($content)) > 0"/>

            <xsl:choose>
                <xsl:when test="not($nonempty_content)">
                    <span class="tbd"><xsl:value-of select="$proteus:lang_TBD_expanded"/></span>
                </xsl:when>
                <xsl:otherwise>
                    <p>
                        <xsl:call-template name="generate_markdown">
                            <xsl:with-param name="content" select="$content"/>
                        </xsl:call-template>
                    </p>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

</xsl:stylesheet>