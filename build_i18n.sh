#! /bin/sh
I18NDUDE=i18ndude
I18NDOMAIN="collective.ploneqrcode"
# find the locales dir
LOCALES=`find . -type d | grep $I18NDOMAIN | grep -m 1 "locales"`
SOURCE=`dirname $LOCALES`;
# rebuild pot file for package's domain and merge it with any manual translations needed
$I18NDUDE rebuild-pot --pot $LOCALES/$I18NDOMAIN.pot --merge $LOCALES/manual.pot --create $I18NDOMAIN $SOURCE
# synchronise translations for package's domain
for po in $LOCALES/*/LC_MESSAGES/$I18NDOMAIN.po; do
$I18NDUDE sync --pot $LOCALES/$I18NDOMAIN.pot $po
done
# rebuild pot file for Plone's domain
$I18NDUDE rebuild-pot --pot $LOCALES/plone.pot --create plone $SOURCE/configure.zcml $SOURCE/profiles/default
# synchronise translations for Plone's domain
for po in $LOCALES/*/LC_MESSAGES/plone.po; do
$I18NDUDE sync --pot $LOCALES/plone.pot $po
done
