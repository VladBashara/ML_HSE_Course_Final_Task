# Модель развернута на https://ml-hse-course-final-task.onrender.com

# Пример работы для сообщения со спамом

```
curl -s -X POST https://ml-hse-course-final-task.onrender.com/predict -H "Content-Type: application/json" -d '{"text":"Here'\''s the hottest thing in DVDs. Now you can make a personal backup copy of a DVD right onto CD-R. Our Hot new software easily takes you through the steps to make a copy of your own DVDs. NOW INCLUDED FOR FREE! Copy PLAYSTATION, MUSIC/MP3s and all Software. - Step by Step Interactive Instructions - All Software Tools Included On CD - No DVD Burner Required - FREE Live Technical Support - 30 Day Risk Free Trial Available - FREE Dvd Movie of your choice (LIMITED TIME OFFER!) We have All the software you need to COPY your own DVD Movies. http://sam.mothost.com/pos/dvd.htm ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ This email has been screened and filtered by our in house OPT-OUT system in compliance with state laws. If you wish to OPT-OUT from this mailing as well as the lists of thousands of other email providers please visit http://sam.mothost.com/pos/optoutd.html ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 8429ZKZm5-584blan2826zxaD1-138BmnT6098TIco7-220rikg3620l52","sender_domain":"spam1.com"}'

{"score":0.999782344068636,"label":1,"is_spam":true,"source":"layer1"}
```

# Пример работы для сообщения без спама
```
curl -s -X POST https://ml-hse-course-final-task.onrender.com/predict -H "Content-Type: application/json" -d '{"text":"*Politics:* Tony Blair has distanced himself from a minister accused of meddling in an election for the leadership of the Labour party'\''s biggest trade union affiliate.","sender_domain":"rssfeeds@jmason.org"}'

{"score":0.0171174984602768,"label":0,"is_spam":false,"source":"layer1"}
```