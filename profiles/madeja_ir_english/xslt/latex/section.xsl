<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>
    <!-- ============================================= -->
    <!-- section template                              -->
    <!-- ============================================= -->

    <xsl:template match="object[@classes='section']">
        <!-- Nesting level -->
        <xsl:param name="nesting_level" select="1"/>
        <xsl:param name="previous_index" select="''"/>

        <xsl:if test="$nesting_level = 1">
            <xsl:text>\section{</xsl:text>
        </xsl:if>
        
        <xsl:if test="$nesting_level = 2">
            <xsl:text>\subsection{</xsl:text>
        </xsl:if>

        <xsl:if test="$nesting_level >= 3">
            <xsl:text>\subsubsection{</xsl:text>
        </xsl:if>
        
        <xsl:value-of select="properties/*[@name=':Proteus-name']"/>

        <xsl:text>}</xsl:text>

    </xsl:template>
</xsl:stylesheet>