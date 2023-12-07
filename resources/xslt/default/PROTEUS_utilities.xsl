<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_document.xsl                           -->
<!-- Content : PROTEUS XSLT for subjects at US - utilities    -->
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

    <!-- Base URL for icons -->
    <xsl:variable name="base_url_icons">https://cdn.jsdelivr.net/gh/amador-duran-toro/remus/assets/images/icons/</xsl:variable>

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
        <xsl:value-of select="proteus-utils:generate_markdown($content)" disable-output-escaping="yes"/>
    </xsl:template>


    <!-- ============================================= -->
    <!-- generate_markdown_row template                -->
    <!-- ============================================= -->

    <xsl:template name="generate_markdown_row">
        <xsl:param name="id" />
        <xsl:param name="label" />
        <xsl:param name="content" />
        <xsl:param name="mandatory" select="false()"/>
        <xsl:param name="span" select="1"/>

        <xsl:variable name="nonempty_content" select="string-length(normalize-space($content)) > 0"/>

        <xsl:if test="$nonempty_content or $mandatory">
            <tr id="{$id}">
                <th>
                    <xsl:value-of select="$label"/>
                </th>
                <td colspan="{$span}">
                    <xsl:choose>
                        <xsl:when test="not($nonempty_content)">
                            <span class="tbd"><xsl:value-of select="$proteus:lang_TBD_expanded"/></span>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:call-template name="generate_markdown">
                                <xsl:with-param name="content" select="$content"/>
                            </xsl:call-template>
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_simple_row template (no markdown)    -->
    <!-- ============================================= -->

    <xsl:template name="generate_simple_row">
        <xsl:param name="id" />
        <xsl:param name="label" />
        <xsl:param name="content" />
        <xsl:param name="mandatory" select="false()"/>
        <xsl:param name="span"      select="1"/>

        <xsl:variable name="nonempty_content" select="string-length(normalize-space($content)) > 0"/>

        <xsl:if test="$nonempty_content or $mandatory">
            <tr id="{$id}">
                <th><xsl:value-of select="$label"/></th>
                <td colspan="{$span}">
                    <xsl:choose>
                        <xsl:when test="not($nonempty_content)">
                            <span class="tbd"><xsl:value-of select="$proteus:lang_TBD_expanded"/></span>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:apply-templates select="$content"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>


    <!-- ============================================= -->
    <!-- generate_header template                      -->
    <!-- ============================================= -->

    <xsl:template name="generate_header">
        <xsl:param name="class" />
        <xsl:param name="icon"  select="concat($class,'.png')"/>
        <xsl:param name="postfix"/>
        <xsl:param name="label"/>
        <xsl:param name="span"  select="1"/>

        <thead>
            <tr>
                <th>
                    <img src="{concat($base_url_icons,$icon)}"/>
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="$label"/>
                </th>
                <th class="name_column" colspan="{$span}">
                    <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']"/>
                    <xsl:if test="$postfix"><xsl:text> </xsl:text><xsl:value-of select="$postfix"/></xsl:if>
                </th>
            </tr>
        </thead>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_software_requirement_header template -->
    <!-- ============================================= -->

    <xsl:template name="generate_software_requirement_expanded_header">
        <xsl:param name="class" select="default"/>
        <xsl:param name="postfix"/>
        <xsl:param name="span"  select="1"/>

        <xsl:variable name="label">
            <xsl:value-of select="properties/codeProperty[@name = ':Proteus-code']/prefix" />
            <xsl:value-of select="properties/codeProperty[@name = ':Proteus-code']/number" />
            <xsl:value-of select="properties/codeProperty[@name = ':Proteus-code']/suffix" />
        </xsl:variable>

        <xsl:call-template name="generate_header">
            <xsl:with-param name="class"   select="$class"/>
            <xsl:with-param name="label"   select="$label"/>
            <xsl:with-param name="postfix" select="$postfix"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_version_row">
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_trace_row">
            <xsl:with-param name="label"   select="$proteus:lang_authors"/>
            <xsl:with-param name="content" select="traces/traceProperty[@name='created-by']"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_trace_row">
            <xsl:with-param name="label"   select="$proteus:lang_sources"/>
            <xsl:with-param name="content" select="traces/traceProperty[@name='source']"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_expanded_header template             -->
    <!-- ============================================= -->

    <xsl:template name="generate_expanded_header">
        <xsl:param name="class"   select="default"/>
        <xsl:param name="label"/>
        <xsl:param name="postfix"/>
        <xsl:param name="span" select="1"/>

        <xsl:call-template name="generate_header">
            <xsl:with-param name="class"   select="$class"/>
            <xsl:with-param name="label"   select="$label"/>
            <xsl:with-param name="postfix" select="$postfix"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_version_row">
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_trace_row">
            <xsl:with-param name="label"   select="$proteus:lang_authors"/>
            <xsl:with-param name="content" select="traces/traceProperty[@name='created-by']"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>
    </xsl:template>

    <!-- =============================================================== -->
    <!-- Special rows templates                                          -->
    <!-- =============================================================== -->

    <!-- ============================================= -->
    <!-- generate_version_row template                 -->
    <!-- ============================================= -->

    <xsl:template name="generate_version_row">
        <xsl:param name="label"     select="$proteus:lang_version"/>
        <xsl:param name="span"      select="1"/>

        <tr>
            <th><xsl:value-of select="$label"/></th>
            <td colspan="{$span}">
                <xsl:value-of select="properties/floatProperty[@name='version']" />
                <xsl:text> (</xsl:text>
                <xsl:value-of select="properties/dateProperty[@name=':Proteus-date']" />
                <xsl:text>)</xsl:text>
            </td>
        </tr>

    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_trace_row template                   -->
    <!-- ============================================= -->

    <xsl:template name="generate_trace_row">
        <xsl:param name="label" />
        <xsl:param name="content" />
        <xsl:param name="mandatory" select="false()"/>
        <xsl:param name="span">1</xsl:param>

        <xsl:if test="$content/trace or $mandatory">
            <tr>
                <th><xsl:value-of select="$label"/></th>
                <td colspan="{$span}">
                    <xsl:choose>
                        <xsl:when test="not($content/trace)">
                            <span class="tbd"><xsl:value-of select="$proteus:lang_TBD_expanded"/></span>
                        </xsl:when>
                        <xsl:otherwise>
                            <ul class="stakeholders">
                                <xsl:apply-templates select="$content"/>
                            </ul>
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_priority_rows template               -->
    <!-- ============================================= -->

    <xsl:template name="generate_priority_rows">
        <xsl:param name="span" select="1"/>

        <xsl:if test="properties/enumProperty[@name='importance'] != 'nd'">
            <xsl:call-template name="generate_simple_row">
                <xsl:with-param name="label"   select="$proteus:lang_importance"/>
                <xsl:with-param name="content" select="properties/enumProperty[@name='importance']"/>
                <xsl:with-param name="span"    select="$span"/>
            </xsl:call-template>
        </xsl:if>

        <xsl:if test="properties/enumProperty[@name='urgency'] != 'nd'">
            <xsl:call-template name="generate_simple_row">
                <xsl:with-param name="label"   select="$proteus:lang_urgency"/>
                <xsl:with-param name="content" select="properties/enumProperty[@name='urgency']"/>
                <xsl:with-param name="span"    select="$span"/>
            </xsl:call-template>
        </xsl:if>

        <xsl:if test="properties/enumProperty[@name='development-status'] != 'nd'">
            <xsl:call-template name="generate_simple_row">
                <xsl:with-param name="label"   select="$proteus:lang_status"/>
                <xsl:with-param name="content" select="properties/enumProperty[@name='development-status']"/>
                <xsl:with-param name="span"    select="$span"/>
            </xsl:call-template>
        </xsl:if>

        <xsl:if test="properties/enumProperty[@name='stability'] != 'nd'">
            <xsl:call-template name="generate_simple_row">
                <xsl:with-param name="label"   select="$proteus:lang_stability"/>
                <xsl:with-param name="content" select="properties/enumProperty[@name='stability']"/>
                <xsl:with-param name="span"    select="$span"/>
            </xsl:call-template>
        </xsl:if>

    </xsl:template>

    <!-- =============================================================== -->
    <!-- Template match for proteus properties                           -->
    <!-- =============================================================== -->

    <!-- ============================================= -->
    <!-- traceProperty                                 -->
    <!-- ============================================= -->
    <xsl:template match="traceProperty">
        <xsl:param name="list_mode" select="true()"/>

        <xsl:for-each select="trace">
            <xsl:variable name="targetId" select="@target" />
            <xsl:variable name="targetObject" select="//object[@id = $targetId]" />

            <xsl:if test="$targetObject">
                <xsl:choose>
                    <xsl:when test="$list_mode">
                        <li>
                            <a href="#{$targetId}">
                                <xsl:value-of select="$targetObject/properties/stringProperty[@name = ':Proteus-name']" />
                            </a>
                        </li>
                    </xsl:when>
                    <xsl:otherwise>
                        <p>
                            <a href="#{$targetId}">
                                <xsl:value-of select="$targetObject/properties/stringProperty[@name = ':Proteus-name']" />
                            </a>
                        </p>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>