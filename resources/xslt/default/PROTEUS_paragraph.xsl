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
        <div id="{@id}" class="proteus-area">
            <xsl:choose>
                <xsl:when test="properties/booleanProperty[@name='is-glossary'] = 'true'">
                    <xsl:call-template name="create_glossary_item"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="create_paragraph"/>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <!-- Paragraph generator template -->
    <xsl:template name="create_paragraph">
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
    </xsl:template>

    <!-- Glossary item generator template -->
    <xsl:template name="create_glossary_item">
        <p>
            <strong>
                <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']"/>
                <xsl:text>: </xsl:text>
            </strong>

            <xsl:variable name="description" select="properties/markdownProperty[@name='text']"/>
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
    </xsl:template>


</xsl:stylesheet>