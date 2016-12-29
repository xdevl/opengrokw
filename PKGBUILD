# Maintainer: xdevl <xdevl@users.noreply.github.com>
pkgname=opengrok
pkgver=0.12.1.6
pkgrel=2
pkgdesc="A fast and usable source code search and cross reference engine, written in Java"
url="http://opengrok.github.io/OpenGrok/"
arch=('any')
license=('CDDL')
depends=('tomcat8' 'sh' 'java-environment' 'ctags' 'python3')
source=("https://github.com/OpenGrok/OpenGrok/files/467358/${pkgname}-${pkgver}.tar.gz.zip"
        'opengrokw.py'
        'opengrokw')
sha1sums=('4bec1b2ae58131fb407b9ca8f18ac330b8624180'
          'd3a3ee2443590f488506230f328aea7375ce461d'
          '8a174d227dcc58af81184ea9b2fbfbbb0bc11f60')

prepare() {
  bsdtar xf ${pkgname}-${pkgver}.tar.gz
}

package() {
	
  _basedir="${pkgname}-${pkgver}"
  install -dm755 "$pkgdir/usr/share/java/opengrok"
  cp -r "${_basedir}/lib"/* "$pkgdir/usr/share/java/opengrok"

  install -dm755 "$pkgdir/usr/share/doc/opengrok"
  cp -r "${_basedir}/doc"/* "$pkgdir/usr/share/doc/opengrok"
  
  install -Dm755 "opengrokw.py" "$pkgdir/usr/share/opengrokw/opengrokw.py"
  install -Dm755 "opengrokw" "$pkgdir/usr/bin/opengrokw"
}
