<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_paragraph.xsl                          -->
<!-- Content : PROTEUS XSLT for subjects at US - paragraph    -->
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
    exclude-result-prefixes="proteus"
>
    
    <!-- =========================================================== -->
    <!-- paragraph template                                      -->
    <!-- =========================================================== -->

    <xsl:template match="object[@classes='paragraph']">
        <div id="{@id}">
            <p>
                <xsl:call-template name="generate_markdown">
                    <xsl:with-param name="content" select="properties/markdownProperty[@name='text']"/>
                </xsl:call-template>
            </p>
        </div>
    </xsl:template>

    <!-- =========================================================== -->
    <!-- paragraph template in "part" mode                       -->
    <!-- =========================================================== -->

    <!-- This approach is better than using a section for parts.     -->
    <!-- It does not break section numbering.                        -->

    <xsl:template match="object[@classes='paragraph']" mode="part">
        <xsl:call-template name="pagebreak"/>
        <div id="{@id}" class="part">
            <xsl:value-of select="text"/><xsl:text> </xsl:text>
            <xsl:number count="//object[@classes='paragraph']" format="I"/>
        </div>
        <xsl:call-template name="pagebreak"/>
    </xsl:template>

    <!-- =========================================================== -->
    <!-- paragraph template in "toc" mode for "parts"            -->
    <!-- =========================================================== -->

    <xsl:template match="object[@classes='paragraph']" mode="toc">
        <br/><br/>
        <li>
            <xsl:value-of select="text"/><xsl:text> </xsl:text>
            <xsl:number count="//object[@classes='paragraph']" format="I"/>
            <a href="#{@id}"><xsl:value-of select="properties/stringProperty[@name='name']"/></a>
        </li>
        <br/><br/>
    </xsl:template>


</xsl:stylesheet>