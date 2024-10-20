<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : association.xsl                                -->
<!-- Content : PROTEUS defualt XSLT for association           -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/08/02                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/10/20 (Amador Durán)                      -->
<!-- Code review and refactoring.                             -->
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
    <!-- ============================================== -->
    <!-- association template                           -->
    <!-- ============================================== -->

    <xsl:template match="object[contains(@classes,'association')]">

        <div id="{@id}" data-proteus-id="{@id}" class="association">

            <table class="association remus_table">

                <xsl:variable name="name">
                    <xsl:call-template name="generate-association-name"/>
                </xsl:variable>

                <!-- Header -->
                <xsl:call-template name="generate_header">
                    <xsl:with-param name="label" select="properties/*[@name=':Proteus-code']"/>
                    <xsl:with-param name="class" select="'association'"/>
                    <xsl:with-param name="name"  select="$name" />
                </xsl:call-template>

                <!-- Association information -->
                <tr>
                    <td colspan="2">
                        <div class="code">
                            <xsl:apply-templates select="." mode="code"/>
                        </div>
                    </td>
                </tr>

                <!-- Comments -->
                <xsl:for-each select="properties/*[@name='comments']">
                    <xsl:call-template name="generate_property_row"/>
                </xsl:for-each>
            </table>
        </div>
    </xsl:template>

    <!-- ============================================== -->
    <!-- association template (code mode)               -->
    <!-- ============================================== -->

    <xsl:template match="object[contains(@classes,'association')]" mode="code">

        <!-- Description -->
        <xsl:variable name="description" select="properties/*[@name='description']"/>
        <xsl:if test="string-length($description)">
            <xsl:call-template name="generate-code-description">
                <xsl:with-param name="multiline-comment" select="true()"/>
            </xsl:call-template>
        </xsl:if>

        <!-- Association declaration -->
        <xsl:variable name="name">
            <xsl:call-template name="generate-association-name"/>
        </xsl:variable>

        <span class="keyword">association </span>
        <span class="class_name"><xsl:value-of select="$name"/></span>

        <!-- Open bracket -->
        <br></br>
        <xsl:text>{</xsl:text>
        <br></br>

        <!-- Roles -->
        <xsl:if test="children/object[@classes='role']">
            <div class="code_comment code_header"><xsl:value-of select="$proteus:lang_code_roles"/></div>
            <ul class="properties">
                <xsl:apply-templates select="children/object[@classes='role']" mode="code"/>
            </ul>
        </xsl:if>

        <br></br>

        <!-- Attributes -->
        <xsl:if test="children/object[@classes='attribute']">
            <div class="code_comment code_header"><xsl:value-of select="$proteus:lang_code_attributes"/></div>
            <ul class="properties">
                <xsl:apply-templates select="children/object[@classes='attribute']" mode="code"/>
            </ul>
        </xsl:if>

        <!-- Close bracket -->
        <br></br>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <!-- ============================================== -->
    <!-- Role template                                  -->
    <!-- ============================================== -->
    <!-- Role template is located in                    -->
    <!-- entity_class.xsl file                          -->

    <!-- ============================================== -->
    <!-- Helper templates                               -->
    <!-- ============================================== -->
    <!-- Helper templates are located in                -->
    <!-- PROTEUS_entity_class.xsl file                   -->

    <xsl:template name="generate-association-name">

        <!-- Name -->
        <xsl:value-of select="properties/stringProperty[@name = ':Proteus-name']"/>

        <xsl:text>( </xsl:text>

        <!-- Get association roles -->
        <xsl:variable name="roles" select="children/object[@classes='role']"/>

        <!-- Include roles -->
        <xsl:for-each select="$roles">
            <xsl:for-each select="properties/traceProperty[@name = 'type']/trace">
                <xsl:variable name="targetId" select="@target" />
                <xsl:variable name="targetObject" select="//object[@id = $targetId]" />
                <xsl:value-of select="$targetObject/properties/stringProperty[@name = ':Proteus-name']" />
            </xsl:for-each>
            <xsl:if test="not(position()=last())">, </xsl:if>
        </xsl:for-each>

        <xsl:choose>
            <xsl:when test="not($roles)">?, ?</xsl:when>
            <xsl:when test="count($roles) = 1">, ?</xsl:when>
        </xsl:choose>

        <xsl:text> )</xsl:text>

    </xsl:template>

</xsl:stylesheet>