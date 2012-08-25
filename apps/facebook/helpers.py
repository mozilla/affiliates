from random import choice, randint

from jingo import register


@register.function
def admin_email_signature():
    salute = choice(['Cheers!', 'Engage,', 'Excelsior!', 'Carry on,',
                     'See you space cowboy...', 'STEVE HOLT,',
                     'Great shot kid, that was one in a million!'])
    rank = choice(['Junior', 'Senior', 'Head', 'Lead'])
    role = choice(['Commandant', 'Subcommander', 'Magistrate', 'Scribe',
                   'Attendant', 'Luthier', 'Codesmith', 'Affiliate', 'Pilot'])
    num = randint(0, 1024)
    division = choice(['', ', Civilian Corps.', ', Eastern Operations',
                       'Red Squadron', ', Order of the Northern Sky (Hokuten)'])
    return ('%s\n-%s %s #%s of The Most Glorious and Excellent Affiliate Army%s'
            % (salute, rank, role, num, division))
