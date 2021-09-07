# Maintainer: xdevl <xdevl@users.noreply.github.com>
pkgname=opengrok
pkgver=1.7.17
pkgrel=1
pkgdesc="A fast and usable source code search and cross reference engine, written in Java"
url="http://opengrok.github.io/OpenGrok/"
arch=('any')
license=('CDDL')
depends=('tomcat10' 'sh' 'java-environment' 'ctags' 'python3')
source=("https://github.com/oracle/opengrok/releases/download/${pkgver}/${pkgname}-${pkgver}.tar.gz"
        'opengrokw.py'
        'opengrokw')
sha1sums=('9ac03eca9e099d8f546fee97d2528cb32b6e4fac'
          'e46be9629862b9b5f4242f191a948e609bb47720'
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
