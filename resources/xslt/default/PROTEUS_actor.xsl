<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_actor.xsl                              -->
<!-- Content : PROTEUS XSLT for subjects at US - actor        -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/07                                     -->
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

    <!-- ============================================= -->
    <!-- proteus:actor template                        -->
    <!-- ============================================= -->

    <xsl:template match="object[@classes='product-requirement actor']">

        <xsl:variable name="label_number">
            <xsl:number from="object[@classes='Proteus-document']"
                count="object[@classes='product-requirement actor']"
                level="any" format="001" />
        </xsl:variable>

        <div id="{@id}">
            <table class="actor remus_table">

                <xsl:call-template name="generate_expanded_header">
                    <xsl:with-param name="label"   select="concat('ACT-',$label_number)"/>
                    <xsl:with-param name="class"   select="'actor'"/>
                </xsl:call-template>

                <xsl:call-template name="generate_simple_row">
                    <xsl:with-param name="label"   select="$proteus:lang_role"/>
                    <xsl:with-param name="content" select="properties/stringProperty[@name='role']"/>
                </xsl:call-template>

                <xsl:call-template name="generate_markdown_row">
                    <xsl:with-param name="label"   select="$proteus:lang_description"/>
                    <xsl:with-param name="content" select="properties/markdownProperty[@name='description']"/>
                </xsl:call-template>

                <xsl:call-template name="generate_comments_row"/>

            </table>
        </div>
    </xsl:template>

</xsl:stylesheet>
