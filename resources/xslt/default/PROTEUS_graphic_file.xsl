<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_graphic_file.xsl                       -->
<!-- Content : PROTEUS XSLT for subjects at US - graphic file -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
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

<!-- ======================================================== -->
<!-- graphic-file template                                    -->
<!-- ======================================================== -->

<xsl:template match="object[@classes='graphic-file']">

    <div id="{@id}" class="figure">
        <!-- Get file name with extension -->
        <xsl:variable name="file_name" select="properties/fileProperty[@name='file']"/>
        <!-- Get the file extension -->
        <xsl:variable name="image_extension" select="substring-after($file_name, '.')" />

        <!-- Get the file encoded base64 -->
        <xsl:variable name="image" select="proteus-utils:image_to_base64($file_name)"/>

        <!-- Build src attribute prefix based on the extension -->
        <xsl:variable name="src_prefix">
            <xsl:choose>
                <xsl:when test="$image_extension = 'png'">data:image/png;base64,</xsl:when>
                <xsl:when test="$image_extension = 'jpg'">data:image/jpeg;base64,</xsl:when>
                <xsl:when test="$image_extension = 'jpeg'">data:image/jpeg;base64,</xsl:when>
                <xsl:when test="$image_extension = 'gif'">data:image/gif;base64,</xsl:when>
                <xsl:when test="$image_extension = 'svg'">data:image/svg+xml;base64,</xsl:when>
                <xsl:otherwise>data:image/jpeg;base64,</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <img class="figure_image">
            <xsl:attribute name="src">
                <xsl:value-of select="concat($src_prefix, $image)" disable-output-escaping="yes"/>
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
                    count="object[@classes='external-resource'] | object[@classes='graphic-file']"
                    level="any"/>:
                <xsl:text> </xsl:text>
            </span>
            
            <!-- applying markdown -->
            <xsl:call-template name="generate_markdown">
                <xsl:with-param name="content" select="properties/markdownProperty[@name='description']"/>
            </xsl:call-template>
        </p>

    </div>

</xsl:template>

</xsl:stylesheet>