<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_section.xsl                            -->
<!-- Content : PROTEUS XSLT for subjects at US - appendix     -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2024/07/29                                     -->
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


    <!-- ============================================= -->
    <!-- appendix template                             -->
    <!-- ============================================= -->

    <xsl:template match="object[@classes='appendix']">
        <!-- Nest level -->
        <xsl:param name="nest_level" select="1"/>

        <div id="{@id}"  data-proteus-id="{@id}">

            <!-- Calculate appendix index -->
            <xsl:variable name="appendix_index">
                <xsl:number level="single" count="object[@classes='appendix']" format="A" />
            </xsl:variable>

            
            <xsl:element name="h1">
                <xsl:value-of select="$appendix_index"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']"/><xsl:apply-templates select="name"/>
            </xsl:element>

            <!-- Apply templates to all section passing the  -->
            <xsl:apply-templates select="children/object">
                <!-- Provide nest level context to children -->
                <xsl:with-param name="nest_level" select="$nest_level + 1"/>
                <xsl:with-param name="previous_index" select="$appendix_index"/>
            </xsl:apply-templates>
            
        </div>
    </xsl:template>

    <!-- ============================================= -->
    <!-- appendix template in "toc" mode               -->
    <!-- ============================================= -->

    <!-- A <ul> parent element is assumed              -->

    <xsl:template match="object[@classes='appendix']" mode="toc">
        <!-- Calculate appendix index -->
        <xsl:variable name="appendix_index">
            <xsl:number level="single" count="object[@classes='appendix']" format="A" />
        </xsl:variable>
        <li>
            <xsl:value-of select="$appendix_index"/>
            <xsl:text> </xsl:text>
            <a href="#{@id}"><xsl:apply-templates select="properties/stringProperty[@name=':Proteus-name']"/></a>
        </li>
        <xsl:if test="children/object[@classes='section']">
            <ul class="toc_list">
                <xsl:apply-templates select="children/object[@classes='section']" mode="toc">
                    <xsl:with-param name="previous_index" select="$appendix_index"/>
                </xsl:apply-templates>
            </ul>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>