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
        <xsl:param name="oid" />
        <xsl:param name="label_class" />
        <xsl:param name="label" select="local-name()"/>
        <xsl:param name="prefix" />
        <xsl:param name="space_after_prefix" select="true()"/>
        <xsl:param name="content_class" />
        <xsl:param name="content" select="."/>
        <xsl:param name="postfix" />
        <xsl:param name="space_before_postfix" select="false()"/>
        <xsl:param name="span" select="1"/>
        <xsl:param name="mode" select="'inline'"/>

        <tr>
            <xsl:if test="$oid">
                <xsl:attribute name="id"><xsl:value-of select="$id"/></xsl:attribute>
            </xsl:if>
            <th>
                <xsl:if test="$label_class">
                    <xsl:attribute name="class">
                        <xsl:value-of select="$label_class"/>
                    </xsl:attribute>
                </xsl:if>
                <xsl:value-of select="$label"/>
            </th>
            <td colspan="{$span}">
                <xsl:call-template name="generate_markdown">
                    <xsl:with-param name="content" select="$content"/>
                </xsl:call-template>
            </td>
        </tr>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_simple_row template (no markdown)    -->
    <!-- ============================================= -->

    <xsl:template name="generate_simple_row">
        <xsl:param name="label"     select="local-name()"/>
        <xsl:param name="content"   select="."/>
        <xsl:param name="mandatory" select="false()"/>
        <xsl:param name="span"      select="1"/>

        <xsl:variable name="nonempty_content" select="string-length(normalize-space($content)) > 0"/>

        <xsl:if test="$nonempty_content or $mandatory">
            <tr>
                <th><xsl:value-of select="$label"/></th>
                <td colspan="{$span}"><xsl:apply-templates select="$content"/></td>
            </tr>
        </xsl:if>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_stakeholders template                -->
    <!-- ============================================= -->

    <xsl:template name="generate_stakeholders">
        <xsl:param name="label"     select="local-name()"/>
        <xsl:param name="content"   select="."/>
        <xsl:param name="mandatory" select="false()"/>
        <xsl:param name="span">1</xsl:param>

        <xsl:if test="$content or $mandatory">
            <tr>
                <th><xsl:value-of select="$label"/></th>
                <td colspan="{$span}">
                    <xsl:choose>
                        <xsl:when test="not($content)">
                            <span class="tbd"><xsl:value-of select="$proteus:lang_TBD"/></span>
                        </xsl:when>
                        <xsl:otherwise>
                            <ul class="stakeholders">
                                <li>
                                    <xsl:value-of select="properties/stringProperty[@name='createdBy']"/>
                                </li>
                            </ul>
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
        </tr>
        </xsl:if>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_directly_affected_objects template   -->
    <!-- ============================================= -->

    <xsl:template name="generate_directly_affected_objects">
        <tr>
            <th>
                <xsl:value-of select="$proteus:lang_directly_affected_objects"/>
            </th>

            <td>
                <xsl:choose>
                    <xsl:when test="not(proteus:directlyAffects)">
                        <span class="tbd"><xsl:value-of select="$proteus:lang_TBD"/></span>
                    </xsl:when>
                    <xsl:otherwise>
                        <ul class="affected_objects">
                            <xsl:for-each select="id(proteus:directlyAffects/@affected)">
                                <li>
                                    <a href="#{@oid}">
                                        [<xsl:value-of select="@oid"/>] <xsl:value-of select="properties/stringProperty[@name='name']"/>
                                    </a>
                                </li>
                            </xsl:for-each>
                        </ul>
                    </xsl:otherwise>
                </xsl:choose>
            </td>
        </tr>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_indirectly_affected_objects template -->
    <!-- ============================================= -->

    <xsl:template name="generate_indirectly_affected_objects">
        <tr>
            <th>
                <xsl:value-of select="$proteus:lang_indirectly_affected_objects"/>
            </th>

            <td>
                <xsl:choose>
                    <xsl:when test="not(proteus:indirectlyAffects)">
                        <span class="tbd"><xsl:value-of select="$proteus:lang_TBD"/></span>
                    </xsl:when>
                    <xsl:otherwise>
                        <ul class="affected_objects">
                            <xsl:for-each select="id(proteus:indirectlyAffects/@affected)">
                                <li>
                                    <a href="#{@oid}">
                                        [<xsl:value-of select="@oid"/>] <xsl:value-of select="properties/stringProperty[@name='name']"/>
                                    </a>
                                </li>
                            </xsl:for-each>
                        </ul>
                    </xsl:otherwise>
                </xsl:choose>
            </td>
        </tr>
    </xsl:template>

    <!-- ============================== -->
    <!-- generate_alternatives template -->
    <!-- ============================== -->

    <xsl:template name="generate_alternatives">
        <xsl:if test="proteus:alternative">
            <tr>
                <th>
                    <xsl:value-of select="$proteus:lang_alternatives"/>
                </th>

                <td>
                    <ol class="alternatives">
                        <xsl:apply-templates select="proteus:alternative"/>
                    </ol>
                </td>
            </tr>
        </xsl:if>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_comments_row template                    -->
    <!-- ============================================= -->

    <xsl:template name="generate_comments_row">
        <xsl:param name="span" select="1"/>

        <xsl:call-template name="generate_markdown_row">
            <xsl:with-param name="label"   select="$proteus:lang_comments"/>
            <xsl:with-param name="content" select="properties/markdownProperty[@name='comments']"/>
            <xsl:with-param name="content_class" select="'proteus_comments'"/>
            <xsl:with-param name="mode"    select="'paragraph'"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>
    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_header template                      -->
    <!-- ============================================= -->

    <xsl:template name="generate_header">
        <xsl:param name="class" select="local-name()"/>
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
                    <xsl:value-of select="properties/stringProperty[@name='name']"/>
                    <xsl:if test="$postfix"><xsl:text> </xsl:text><xsl:value-of select="$postfix"/></xsl:if>
                </th>
            </tr>
        </thead>
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

        <xsl:call-template name="generate_simple_row">
            <xsl:with-param name="label"   select="$proteus:lang_version"/>
            <xsl:with-param name="content" select="properties/stringProperty[@name='version']"/>
            <xsl:with-param name="content_class" select="'proteus_version'"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_stakeholders">
            <xsl:with-param name="label"   select="$proteus:lang_authors"/>
            <xsl:with-param name="content" select="properties/stringProperty[@name='createdBy']"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_stakeholders">
            <xsl:with-param name="label"   select="$proteus:lang_sources"/>
            <xsl:with-param name="content" select="properties/stringProperty[@name='sources']"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

    </xsl:template>

    <!-- ============================================= -->
    <!-- generate_priority_rows template               -->
    <!-- ============================================= -->

    <xsl:template name="generate_priority_rows">
        <xsl:param name="span" select="1"/>

        <xsl:call-template name="generate_simple_row">
            <xsl:with-param name="label"   select="$proteus:lang_importance"/>
            <xsl:with-param name="content" select="id(proteus:importance/@value)/proteus:name"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_simple_row">
            <xsl:with-param name="label"   select="$proteus:lang_urgency"/>
            <xsl:with-param name="content" select="id(proteus:urgency/@value)/proteus:name"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_simple_row">
            <xsl:with-param name="label"   select="$proteus:lang_status"/>
            <xsl:with-param name="content" select="id(proteus:status/@value)/proteus:name"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

        <xsl:call-template name="generate_simple_row">
            <xsl:with-param name="label"   select="$proteus:lang_stability"/>
            <xsl:with-param name="content" select="id(proteus:stability/@value)/proteus:name"/>
            <xsl:with-param name="span"    select="$span"/>
        </xsl:call-template>

    </xsl:template>

</xsl:stylesheet>