import os


def __virtual__():
    return 'nginx_site' if __salt__['cmd.has_exec']('nginx') else False


def enabled(name):
    ret = {'changes': {}, 'comment': '', 'name': name, 'result': True}
    if not __salt__['nginx_site.exists'](name):
        return _fail(ret, '{} site does not exist'.format(name))
    if __salt__['nginx_site.is_enabled'](name):
        return _success(ret, '{} site is already enabled'.format(name))
    result, comment = __salt__['nginx_site.enable'](name)
    if not result:
        return _fail(ret, comment)
    return _success(ret, comment, enabled=name)


def disabled(name):
    ret = {'changes': {}, 'comment': '', 'name': name, 'result': True}
    if not __salt__['nginx_site.exists'](name):
        return _fail(ret, '{} site does not exist'.format(name))
    if not __salt__['nginx_site.is_enabled'](name):
        return _success(ret, '{} site is already disabled'.format(name))
    result, comment = __salt__['nginx_site.disable'](name)
    if not result:
        return _fail(ret, comment)
    return _success(ret, comment, disabled=name)


def managed(
        name,
        source=None,
        source_hash=None,
        template=None,
        context=None,
        defaults=None,
        enable=False,
        **kwargs):
    env = kwargs.get('__env__', 'base')
    if __opts__['test']:
        ret['result'], ret['comment'] = __salt__['nginx_site.check_managed'](
            name=name,
            source=source,
            source_hash=source_hash,
            template=template,
            context=context,
            defaults=defaults,
            env=env,
            **kwargs
        )
        return ret
    ret = __salt__['nginx_site.manage'](
        name=name,
        source=source,
        source_hash=source_hash,
        template=template,
        context=context,
        defaults=defaults,
        env=env,
        **kwargs
    )
    if not ret['result']:
        return ret

    if ret['changes']:
        ret['changes']['processed'] = name
    if enable and not __salt__['nginx_site.is_enabled'](name):
        result, comment = __salt__['nginx_site.enable'](name)
        if not result:
            return _fail(ret, comment)
        changes = {'enabled': name}
        return _success(ret, comment, enabled=name)
    return _success(ret, '')


def absent(name):
    ret = {'changes': {}, 'comment': '', 'name': name, 'result': True}
    if not __salt__['nginx_site.exists'](name):
        return _success(ret, '{} site does not exist'.format(name))
    result, comment = __salt__['nginx_site.remove'](name)
    if not result:
        return _fail(ret, comment)
    return _success(ret, comment, removed=name)


def _update_comment(ret, comment):
    if ret['comment']:
        comment = '\n'.join([ret['comment'], comment])
    ret['comment'] = comment
    return ret


def _success(ret, comment, **changes):
    if comment:
        _update_comment(ret, comment)
    ret['changes'].update(changes)
    return ret


def _fail(ret, comment):
    _update_comment(ret, comment)
    ret['result'] = False
    return ret
