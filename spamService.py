# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 02:20:31 2020
@author: Venkata N Divi
"""

import spamcheck,time,sys,re

htmlTags = [
    '<!–-','<!DOCTYPE>','<!doctype>','<a>','<abbr>','<acronym>','<address>','<applet>','<area>','<article>',
    '<aside>','<audio>','<b>','<base>','<basefont>','<bb>','<bdi>','<bdo>','<big>','<blockquote>','<body>',
    '<br>','<button>','<canvas>','<caption>','<center>','<cite>','<code>','<col>','<colgroup>','<command>',
    '<data>','<datagrid>','<datalist>','<dd>','<del>','<details>','<dfn>','<dialog>','<dir>','<div>','<dl>',
    '<dt>','<em>','<embed>','<eventsource>','<fieldset>','<figcaption>','<figure>','<font>','<footer>','<form>',
    '<frame>','<frameset>','<h1>','<h2>','<h3>','<h4>','<h5>','<h6>','<head>','<header>','<hgroup>','<hr>',
    '<html>','<i>','<iframe>','<img>','<input>','<ins>','<isindex>','<kbd>','<keygen>','<label>','<legend>',
    '<li>','<link>','<main>','<map>','<mark>','<menu>','<menuitem>','<meta>','<meter>','<nav>','<noframes>',
    '<noscript>','<object>','<ol>','<optgroup>','<option>','<output>','<p>','<param>','<pre>','<progress>',
    '<q>','<rb>','<rp>','<rt>','<rtc>','<ruby>','<s>','<samp>','<script>','<section>','<select>','<small>',
    '<source>','<span>','<strike>','<strong>','<style>','<sub>','<summary>','<sup>','<table>','<tbody>','<td>',
    '<template>','<textarea>','<tfoot>','<th>','<thead>','<time>','<title>','<tr>','<track>','<tt>','<u>','<ul>',
    '<var>','<video>','<wbr>','<!DOCTYPE ','<!doctype ','<a ','<abbr ','<acronym ','<address ','<applet ','<area ',
    '<article ','<aside ','<audio ','<b ','<base ','<basefont ','<bb ','<bdi ','<bdo ','<big ','<blockquote ','<body ',
    '<br ','<button ','<canvas ','<caption ','<center ','<cite ','<code ','<col ','<colgroup ','<command ','<data ',
    '<datagrid ','<datalist ','<dd ','<del ','<details ','<dfn ','<dialog ','<dir ','<div ','<dl ','<dt ','<em ',
    '<embed ','<eventsource ','<fieldset ','<figcaption ','<figure ','<font ','<footer ','<form ','<frame ','<frameset ',
    '<h1 ','<h2 ','<h3 ','<h4 ','<h5 ','<h6 ','<head ','<header ','<hgroup ','<hr ','<html ','<i ','<iframe ','<img ',
    '<input ','<ins ','<isindex ','<kbd ','<keygen ','<label ','<legend ','<li ','<link ','<main ','<map ','<mark ',
    '<menu ','<menuitem ','<meta ','<meter ','<nav ','<noframes ','<noscript ','<object ','<ol ','<optgroup ','<option ',
    '<output ','<p ','<param ','<pre ','<progress ','<q ','<rb ','<rp ','<rt ','<rtc','<ruby ','<s ','<samp ','<script ',
    '<section ','<select ','<small ','<source ','<span ','<strike ','<strong ','<style ','<sub ','<summary ','<sup ',
    '<table ','<tbody ','<td ','<template ','<textarea ','<tfoot ','<th ','<thead ','<time ','<title ','<tr ','<track ',
    '<tt ','<u ','<ul ','<var ','<video ','<wbr ']

class spamClassification():
    def __init__(self):
        print ("init") 
        
    def getHTMLContent(self,mainData):
        htmlData = ''
        try:
            if '--000000000000' in mainData:
                mainData = mainData.split('--000000000000')[1:]
                for dd in mainData:
                    if 'Content-Type: text/html;' in dd:
                        mainData = '\n'.join(dd.strip() for dd in mainData[mainData.index(dd):])
                        break
                mainData = '\n'.join(dd.strip() for dd in mainData.splitlines() if len(dd)>1)
                htmlData = ('\n'.join(dd.strip() for dd in mainData.splitlines()[3:-1]))
                if not '<html' in htmlData:
                    htmlData = '<html>\n'+htmlData+'\n</html>'
                
                return htmlData
            else:
                htmlData,ind,start = re.findall(re.compile('<.*?>'),mainData),0,''
                for data in htmlData:
                    for tag in htmlTags:
                        if tag in data:
                            start,ind = data,1
                            break
                    if ind == 1: break
                if start in mainData:
                    mainData  = start+'\n'.join(dd.strip() for dd in mainData.split(start)[1:] if len(dd)>1)
                    htmlData = ('\n'.join(dd.strip() for dd in mainData.splitlines() if len(dd)>1))
                    if not '<html' in htmlData:
                        htmlData = '<html>\n'+htmlData+'\n</html>'
                    
                    return htmlData
                else:
                    return mainData
                
            return mainData
        except Exception as e:
            print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception, e)
            return mainData
    
    def runSpamPackage(self,data):
        try:
            count,score,reasons = 0,0,[]
            while count < 5:
                try:
                    count += 1
                    result = spamcheck.check(data, report=True)
                except Exception: time.sleep(2)
                else: break
            else: result = []
                
        except Exception: result = []
        
        try:
            if result and len(result)>0:
                data,spamRes = result['report'].split('\n'),[]
                for dd in data[2:]:
                    if '_' in dd and '.' in dd:
                        strr = dd
                        spamRes.append(strr.strip())
                    else:
                        spamRes.remove(strr.strip())
                        strr = strr.strip()+' '+dd.strip()
                        spamRes.append(strr.strip())
            
                for dd in spamRes:
                    spamRules = dd.split()
                    reasons.append({"Type":spamRules[1], "Description":' '.join(spamRules[2:]).strip(), "Scores for Clause":spamRules[0]})
                
                score += float(result["score"])
            return reasons,score
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),Exception,e)
            return reasons,score
    
    def spamV2finalService(self,fromAddress_,subject_,html_):
        try:
            data,final_result,new_score = '',{},0
            data += 'Received: \nX-Received: \nSubject:'+subject_+'\nDate:Wed, 3 Jun 2020 20:05:22 +0530\nMessage-Id: <0@0.com>\n'
            data += 'MIME-Version: 1.0\nContent-Type: multipart/alternative; charset="UTF-8" boundary="_----------=_15290474107679372\n'
            data += 'Content-Transfer-Encoding: binary\nFrom:'+fromAddress_+'\nTo: \nDKIM-Signature:{}\n_----------=_15290474107679372\n'
            data += 'Content-Type: text/plain; charset="UTF-8"\n_----------=_15290474107679372\n'
            data += 'Content-Type: text/html; charset="UTF-8"\nContent-Transfer-Encoding: quoted-printable\n_----------=_15290474107679372\n'
            
            if html_ and len(html_)>0: data += html_
            data +='\n_----------=_15290474107679372'
            
            reasons,original_spam_score = self.runSpamPackage(data)
            if original_spam_score>=5:
                new_score = ((original_spam_score-2.5)/(5-2.5))+1.5
                new_score = 5 if new_score > 5 else new_score
                print('1: ',new_score)
            elif original_spam_score < 5 and original_spam_score > 0:
                new_score = ((original_spam_score)/(2.5))+0.5
                new_score = 0 if new_score < 0 else new_score
            else:
                new_score = 0
            
            spamClass = 'SPAM' if new_score>=2.5 else 'NOT SPAM'
            final_result["spam_result"] = {"reasons":reasons, "class":spamClass,"score":new_score}
            
            return final_result
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),e)
            