<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_information_requirement.xsl            -->
<!-- Content : PROTEUS XSLT for subjects at US - information  -->
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

    <!-- ============================================== -->
    <!-- Information Requirement template            -->
    <!-- ============================================== -->
    <!-- Note the use of colspan=2                      -->

    <xsl:template match="object[@classes='product-requirement information-requirement']">
        <xsl:variable name="span" select="2"/>

        <div id="{@id}">
            <table class="information_requirement remus_table">

                <xsl:call-template name="generate_expanded_header">
                    <xsl:with-param name="class"   select="'informationRequirement'"/>
                    <xsl:with-param name="span" select="$span"/>
                </xsl:call-template>

                <!-- description -->
                <xsl:call-template name="generate_markdown_row">
                    <xsl:with-param name="label"   select="$proteus:lang_description"/>
                    <xsl:with-param name="content" select="properties/markdownProperty[@name='description']"/>
                    <xsl:with-param name="span" select="$span"/>
                </xsl:call-template>

                <!-- specific data -->
                <!-- TODO: Handle this using child archetypes -->
                <!-- <tr>
                    <th>
                        <xsl:value-of select="$rem:lang_specific_data"/>
                    </th>

                    <td colspan="2">
                        <xsl:choose>
                            <xsl:when test="not(rem:specificData)">
                                <span class="tbd"><xsl:value-of select="$rem:lang_TBD"/></span>
                            </xsl:when>
                            <xsl:otherwise>
                                <ul class="specific_data">
                                    <xsl:apply-templates select="rem:specificData"/>
                                </ul>
                            </xsl:otherwise>
                        </xsl:choose>
                    </td>
                </tr> -->
                <xsl:call-template name="generate_markdown_row">
                    <xsl:with-param name="label"   select="$proteus:lang_specific_data"/>
                    <xsl:with-param name="content" select="properties/markdownProperty[@name='specificData']"/>
                    <xsl:with-param name="span" select="$span"/>
                </xsl:call-template>


                <xsl:call-template name="generate_comments_row">
                    <xsl:with-param name="span" select="$span"/>
                </xsl:call-template>

            </table>
        </div>
    </xsl:template>

</xsl:stylesheet>
