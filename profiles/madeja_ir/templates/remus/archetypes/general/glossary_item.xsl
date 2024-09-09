<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : glossary_item.xsl                              -->
<!-- Content : PROTEUS default XSLT for glossary-item         -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/07 (Amador Durán)                      -->
<!-- match must be object[ends-with(@classes,'glossary-item')]-->
<!-- since glossary-item is a subclass of                     -->
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
    <!-- glossary-item template                                      -->
    <!-- =========================================================== -->

    <xsl:template match="object[contains(@classes,'glossary-item')]">
  
        <div id="{@id}" class="glo" data-proteus-id="{@id}">
            <p>
                <strong>
                    <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']"/>
                    <xsl:text>: </xsl:text>
                </strong>

                <xsl:variable name="description" select="properties/markdownProperty[@name='description']"/>
                <xsl:variable name="nonempty_content" select="string-length(normalize-space($description)) > 0"/>

                <xsl:choose>
                    <xsl:when test="not($nonempty_content)">
                        <span class="tbd"><xsl:value-of select="$proteus:lang_TBD_expanded"/></span>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:call-template name="generate_markdown">
                            <xsl:with-param name="content" select="$description"/>
                        </xsl:call-template>
                    </xsl:otherwise>
                </xsl:choose>
            </p>
        </div>
    </xsl:template>

</xsl:stylesheet>