<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>

    <!-- ============================================= -->
    <!-- pagebreak template                            -->
    <!-- ============================================= -->

    <xsl:template name="pagebreak">
        <div class="page-break"></div>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_markdown template                    -->
    <!-- ============================================= -->

    <xsl:template name="generate_markdown">
        <xsl:param name="content" select="string(.)"/>
        <xsl:value-of select="proteus-utils:glossary_highlight(proteus-utils:generate_markdown($content))" disable-output-escaping="yes"/>
    </xsl:template>

    <!-- ============================================= -->
    <!-- Document separator                            -->
    <!-- ============================================= -->
    <xsl:template match="object[@classes=':Proteus-document']">
        <hr></hr>
        <h2 style="text-align: center;">
            <strong>
                <xsl:text>Document </xsl:text>
                <xsl:number count="object[@classes=':Proteus-document']"/>
                <xsl:text>: </xsl:text>
                <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']" />
            </strong>
        </h2>

        <xsl:apply-templates select="children/object"/>
    </xsl:template>

    <!-- ============================================= -->
    <!-- Default template (do not render)              -->
    <!-- ============================================= -->
    <xsl:template match="object">
        <xsl:apply-templates select="children/object"/>
    </xsl:template>


</xsl:stylesheet>