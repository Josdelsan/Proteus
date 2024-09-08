<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_local_resource.xsl                     -->
<!-- Content : PROTEUS default XSLT for local_resource        -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/08 (Amador Durán)                      -->
<!-- match must be object[ends-with(@classes,'appendix')]     -->
<!-- since appendix is a subclass of section, and its classes -->
<!-- attribute is "section appendix".                         -->
<!-- To check if an object is of a given class:               -->
<!--    object[contains(@classes,class_name)]                 -->
<!-- To check if an object is of a given final class:         -->
<!--    object[ends-with(@classes,class_name)]                -->
<!-- PROBLEM: XSLT 1.0 does not include ends-with             -->
<!-- graphic-file -> local-resource                           -->
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

<!-- ======================================================== -->
<!-- local-resoure template                                   -->
<!-- ======================================================== -->

<xsl:template match="object[contains(@classes,'local-resource')]"> 

    <div id="{@id}" data-proteus-id="{@id}">

        <div class="figure">
            <!-- Get file name with extension -->
            <xsl:variable name="file_name" select="properties/fileProperty[@name='file']"/>

            <!-- Get the image width percentage -->
            <xsl:variable name="image_width_percentage">
                <xsl:choose>
                    <xsl:when test="properties/integerProperty[@name='width']">
                        <xsl:value-of select="properties/integerProperty[@name='width']"/>
                    </xsl:when>
                    <xsl:otherwise>50</xsl:otherwise>
                </xsl:choose>
            </xsl:variable>

            <img class="figure_image">
                <xsl:attribute name="src">
                    <xsl:value-of select="concat('assets:///', $file_name)" disable-output-escaping="no"/>
                </xsl:attribute>

                <xsl:attribute name="style">
                    <xsl:value-of select="concat('width:', $image_width_percentage, '%')"/>
                </xsl:attribute>
            </img>

            <p class="figure_caption">
                <span class="figure_caption_label">
                    <xsl:value-of select="$proteus:lang_figure"/>
                    <xsl:text> </xsl:text>
                    <!-- from is needed to restart numbering in each document          -->
                    <!-- level is needed to avoid restarting numbering in each section -->
                    <xsl:number
                        from="object[@classes=':Proteus-document']"
                        count="object[contains(@classes,'remote-resource')] | object[contains(@classes,'local-resource')]"
                        level="any"/>:
                    <xsl:text> </xsl:text>
                </span>
                
                <!-- applying markdown -->
                <xsl:call-template name="generate_markdown">
                    <xsl:with-param name="content" select="properties/markdownProperty[@name='description']"/>
                </xsl:call-template>
            </p>

        </div>
    </div>

</xsl:template>

</xsl:stylesheet>